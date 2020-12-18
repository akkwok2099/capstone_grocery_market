from flask import session, redirect, flash, abort, \
    request, url_for, render_template, jsonify, Flask
from flask.helpers import make_response
from datetime import datetime
# from werkzeug.datastructures import MultiDict
from models import Aisle, Product, Customer, Purchase, \
    Department, Employee, Supplier, AisleContains
from dtos import EmployeeDto, ProductDto
from sqlalchemy.sql.expression import func
# from auth import requires_login, requires_auth
from flask_cors import CORS, cross_origin
from urllib.parse import urlencode
from flask_sqlalchemy import SQLAlchemy

from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate
from flask_moment import Moment

from functools import wraps
from jose import jwt
from urllib.request import urlopen

import dateutil.parser
import babel
import logging
from logging import FileHandler, Formatter
from config import Config

import json

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(
    __name__,
    static_url_path='/static',
    template_folder='templates')

app.config.from_object(Config)
app.app_context().push()

CORS(app, resources={'/': {'origins': 'http://localhost'}})

app.secret_key = app.config['CLIENT_SECRET']

swagger_bp = get_swaggerui_blueprint(
    app.config['SWAGGER_URL'],
    app.config['API_URL'],
    config={
        'app_name': "UdaciMarket_Management_System"
    }
)

# ---------------------------------------------------------------------------
# Pagination code for displaying database items
# Unused as of now; save for future implementation
# ---------------------------------------------------------------------------
#
# def paginate_items(request, selection):
#     page = request.args.get('page', 1, type=int)
#     start = (page - 1) * ITEMS_PER_PAGE
#     end = start + ITEMS_PER_PAGE

#     products = [product.format() for product in selection]
#     current_products = products[start: end]

#     return current_products

# ----------------------------------------------------------------------------
# Filters
# ----------------------------------------------------------------------------


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    elif format == 'slash':
        format = 'MM/dd/y'
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

app.register_blueprint(swagger_bp, url_prefix='/swagger')

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

conf_profile_key = app.config['PROFILE_KEY']
conf_access_key = app.config['ACCESS_KEY']

db.app = app
db.init_app(app)
migrate.init_app(app, db)
moment.init_app(app)

'''
    Implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=app.config['CLIENT_ID'],
    client_secret=app.config['CLIENT_SECRET'],
    api_base_url=f'https://{app.config["AUTH0_DOMAIN"]}',
    access_token_url=app.config['ACCESS_TOKEN_URL'],
    authorize_url=app.config['AUTHORIZE_URL'],
    client_kwargs={
        'scope': 'openid profile email'
    },
)


def _get_token_auth_header():

    #############################################################
    #
    # TODO This is not the correct way to implement security,
    # I'd imagine that one should be passing the access key
    # between the front end and back end through the request
    # header. However, I have spend two weeks trying different
    # ways and still couldn't come up with a feasible solution.
    # Since this part is not critical for the capstone, I have
    # implemented this temporary solution to force the
    # application to work, and I will try to figure it out in
    # a later time.
    #
    # This implementation does not grab the access token from
    # the request header, but check the host url from the request
    # header and see if it's the same as the 'API Audience' set
    # up using the Auth0 API UI. If it is, grab the access key
    # stored in the Flask session when the application is going
    # through the callback code after logging in. And all the
    # steps after that follow strictly to how we are taught.
    #
    ###############################################################

    api_audience = app.config['API_AUDIENCE']

    if request.headers['HOST'] in api_audience:
        if 'POSTMAN_TOKEN' not in request.headers:
            access_key = session[conf_access_key]
            return access_key['access']
    else:
        if 'Authorization' not in request.headers:
            raise AuthError({
                "code": "authorization_required",
                "description": "Authorization is expected in header"
            }, 401)

    # "Authorization": "bearer <<token>>"
    auth_header = request.headers['Authorization']

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or header_parts[0].lower() != 'bearer':
        raise AuthError({
            "code": "invalid_token",
            "description": "Mendatory authorization requires 'bearer' token"
        }, 401)

    return header_parts[1]


'''
@DONE implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is
    not in the payload permissions array
    return true otherwise
'''


def _check_permissions(permission, payload):
    if 'permissions' not in payload:
        flash('Invalid claims: Permissions not included in JWT', 'danger')
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)

    if isinstance(permission, list) and len(permission) > 1:
        if not set(permission).intersection(payload['permissions']):
            flash('Unauthorized: Permissions not found', 'danger')
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found'
            }, 401)
    else:
        if permission not in payload['permissions']:
            flash('Unauthorized: Permissions not found', 'danger')
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found'
            }, 401)

    return True


'''
    Implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def _verify_decode_jwt(token):
    # Get the public key from Auth0
    jsonurl = urlopen(
        f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose the key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=app.config['ALGORITHMS'],
                audience=app.config['API_AUDIENCE'],
                issuer=(
                    f'https://{app.config["AUTH0_DOMAIN"]}/')
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': ('Incorrect claims. Please check the '
                                'audience and issuer')
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = _get_token_auth_header()
            try:
                payload = _verify_decode_jwt(token)
            except BaseException:
                raise AuthError({
                    "code": "jwt_decode_error",
                    "description": "Error decoding JWT"
                }, 401)

            _check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if app.config['PROFILE_KEY'] not in session:
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


'''
Authorization and Authentication Routes
'''


@app.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=app.config['CALLBACK_URL'],
        audience=app.config['API_AUDIENCE'])


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for(
        'home', _external=True),
        'client_id': app.config['CLIENT_ID']}
    return redirect(f'{auth0.api_base_url}/v2/logout?{urlencode(params)}')


@app.route('/callback')
def callback_handling():
    token = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[app.config['JWT_PAYLOAD']] = userinfo
    session[conf_profile_key] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture'],
        'nickname': userinfo['nickname']
    }
    session[app.config['ID_KEY']] = {'id': token['id_token']}
    session[conf_access_key] = \
        {'access': token['access_token']}

    return render_template(
        'grocery/home.html',
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


'''
Use the after_request decorator to set Access-Control-Allow
'''


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, POST, PATCH, PUT, DELETE, OPTIONS')
    return response


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------


@app.route('/')
@app.route('/home')
@requires_login
def home():
    # -------------------
    # Home page
    # -------------------
    return render_template(
        'grocery/home.html',
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/constructions')
def constructions():
    # -------------------
    # Construction page
    # -------------------
    return render_template(
        'errors/construction.html',
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])

# -------------------------------------------------------
# Aisles
# -------------------------------------------------------


@app.route('/aisles', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:aisle')
def aisles(self):
    # -------------------------
    # List all aisles
    # -------------------------
    aisles = db.session.query(Aisle).order_by(Aisle.aisle_number).all()

    return render_template(
        'grocery/aisles.html', data=aisles)


@app.route('/aisles/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:aisle')
def add_aisle(self):
    # -------------------------
    # Add an aisle
    # -------------------------
    aisle_number = request.form.get('aisle_number', '')
    name = request.form.get('name', '')

    aisle = Aisle(aisle_number=aisle_number, name=name)

    try:
        db.session.add(aisle)
        db.session.commit()
        flash(
            f'Aisle {aisle_number} was successfully added!', 'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Aisle {aisle_number} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'aisles',
        data=db.session.query(Aisle).order_by(
            Aisle.aisle_number).all()))


@app.route('/aisles/<string:aisle_number>', methods=['PUT', 'DELETE', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth(['delete:aisle', 'put:aisle'])
def handle_aisle(self, aisle_number):
    aisle = db.session.query(
        Aisle).filter_by(aisle_number=int(aisle_number)).one_or_none()

    if request.method == 'DELETE':
        # -------------------------
        # Delete an aisle
        # -------------------------

        if aisle is None:
            flash(
                f'No data with Aisle number = {aisle_number} could be found!',
                'danger')
            abort(422)

        try:
            db.session.delete(aisle)
            db.session.commit()
            flash(f'Aisle {aisle_number} was successfully deleted!', 'success')
        except Exception:
            db.session.rollback()
            flash(
                f'An error occurred. Aisle {aisle_number} fail to be deleted!',
                'danger')
        finally:
            db.session.close()

        return redirect(url_for(
            'aisles',
            data=db.session.query(Aisle).order_by(Aisle.aisle_number).all(),
            userinfo=session[conf_profile_key],
            accessinfo=session[conf_access_key]))

    elif request.form.get('_method') == 'PUT':
        # -------------------------
        # Update data of aisle
        # -------------------------

        if aisle is None:
            flash(
                f'No data with Aisle number = {aisle_number} could be found!',
                'danger')
            abort(422)

        aisle.aisle_number = aisle_number
        aisle.name = request.form.get('name')

        try:
            db.session.commit()
            flash(
                f'Aisle {aisle_number} was successfully updated!',
                'success')
        except Exception:
            db.session.rollback()
            flash(
                f'An error occurred. Aisle {aisle_number} \
                could not be updated!',
                'danger')
        finally:
            db.session.close()

        return make_response(redirect(url_for(
            'aisles',
            data=db.session.query(Aisle).order_by(Aisle.aisle_number).all(),
            userinfo=session[conf_profile_key],
            accessinfo=session[conf_access_key])))
    else:
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)


# ----------------------------------------------------------------
# Customers
# ----------------------------------------------------------------

@app.route('/customers', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:customer')
def customers(self):
    # -------------------------
    # List all customers
    # -------------------------
    customers = db.session.query(Customer).order_by(Customer.id).all()

    return render_template(
        'grocery/customers.html', data=customers,
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/customers/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:customer')
def add_customer(self):
    # -------------------------
    # Add a customer
    # -------------------------
    name = request.form.get('name', '')
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')

    max_id = db.session.query(func.max(Customer.id)).one_or_none()
    id = max_id[0] + 1

    customer = Customer(
        id=id,
        name=name,
        phone=phone,
        email=email
    )

    try:
        db.session.add(customer)
        db.session.commit()
        flash(f'Customer {name} was successfully added!', 'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Customer {name} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'customers',
        data=db.session.query(Customer).order_by(
            Customer.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))


@app.route('/customers/<string:customer_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:customer')
def update_customer(self, customer_id):
    # -------------------------
    # Update data of customer
    # -------------------------
    if request.form.get('_method') != 'PUT':
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)

    customer = db.session.query(
        Customer).filter_by(id=int(customer_id)).one_or_none()

    if customer is None:
        flash(
            f'No data with Customer ID = {customer_id} could be found!',
            'danger')
        abort(422)

    customer.id = customer_id
    customer.name = request.form.get('name')
    customer.phone = request.form.get('phone')
    customer.email = request.form.get('email')

    try:
        db.session.commit()
        flash(
            f'Customer {customer_id} was successfully updated!',
            'success')
    except Exception:
        db.session.rollback()
        flash(f'An error occurred. Customer {customer_id} \
            could not be updated!', 'danger')
    finally:
        db.session.close()

    return make_response(redirect(url_for(
        'customers',
        data=db.session.query(Customer).order_by(Customer.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])))


# -------------------------------------------------------
# Departments
# -------------------------------------------------------

@app.route('/departments', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:department')
def departments(self):
    # -------------------------
    # List all departments
    # -------------------------
    departments = db.session.query(Department).order_by(Department.id).all()

    return render_template(
        'grocery/departments.html', data=departments,
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/departments/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:department')
def add_department(self):
    # -------------------------
    # Add a department
    # -------------------------
    name = request.form.get('name', '')

    max_id = db.session.query(func.max(Department.id)).one_or_none()
    id = max_id[0] + 1

    department = Department(
        id=id,
        name=name
    )

    try:
        db.session.add(department)
        db.session.commit()
        flash(
            f'Department {name} was successfully added!',
            'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Department {name} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'departments',
        data=db.session.query(Department).order_by(
            Department.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))


@app.route('/departments/<string:department_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:department')
def update_department(self, department_id):
    # -------------------------
    # Update data of department
    # -------------------------
    if request.form.get('_method') != 'PUT':
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)

    department = db.session.query(
        Department).filter_by(id=int(department_id)).one_or_none()

    if department is None:
        flash(
            f'No data with Department ID = {department_id} could be found!',
            'danger')
        abort(422)

    department.id = department_id,
    department.name = request.form.get('name')

    try:
        db.session.commit()
        flash(
            f'Department {department_id} was successfully updated!',
            'success')
    except Exception:
        db.session.rollback()
        flash(f'An error occurred. Department {department_id} \
            could not be updated!', 'danger')
    finally:
        db.session.close()

    return make_response(redirect(url_for(
        'departments',
        data=db.session.query(Department).order_by(Department.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])))


# ----------------------------------------------------------------
# Employees
# ----------------------------------------------------------------

@app.route('/employees', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:employee')
def employees(self):
    # -------------------------
    # List all employees
    # -------------------------

    dtos = []

    results = db.session.query(
            Employee, Department).filter(
            Employee.department_id == Department.id).order_by(
                Department.id, Employee.id).all()

    for emp, dep in results:
        dto = EmployeeDto(
            id=emp.id,
            name=emp.name,
            department_id=emp.department_id,
            department_name=dep.name,
            title=emp.title,
            emp_number=emp.emp_number,
            address=emp.address,
            phone=emp.phone,
            wage=emp.wage,
            is_active=emp.is_active
        )

        dtos.append(dto)

    return render_template(
        'grocery/employees.html', data=dtos,
        departments=db.session.query(
            Department).order_by(Department.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/employees/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:employee')
def add_employee(self):
    # -------------------------
    # Add an employee
    # -------------------------
    name = request.form.get('name', '')
    department = request.form.get('department_name', '')
    department_id = department.split(' - ', 2)[0]
    title = request.form.get('title', '')
    emp_number = request.form.get('emp_number', '')
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    wage = request.form.get('wage', '')

    max_id = db.session.query(func.max(Employee.id)).one_or_none()
    id = max_id[0] + 1

    employee = Employee(
        id=id,
        name=name,
        department_id=department_id,
        title=title,
        emp_number=emp_number,
        address=address,
        phone=phone,
        wage=wage,
        is_active=True
    )

    try:
        db.session.add(employee)
        db.session.commit()
        flash(
            f'Employee {name} was successfully added!',
            'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Employee {name} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'employees',
        data=db.session.query(Employee).order_by(
            Employee.department_id, Employee.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))


@app.route('/employees/<string:employee_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:employee')
def update_employee(self, employee_id):
    # -------------------------
    # Update data of employee
    # -------------------------
    if request.form.get('_method') != 'PUT':
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)

    employee = db.session.query(
        Employee).filter_by(id=int(employee_id)).one_or_none()

    if employee is None:
        flash(
            f'No data with Employee ID = {employee_id} could be found!',
            'danger')
        abort(422)

    employee.id = employee_id
    employee.name = request.form.get('name')

    temp = request.form.get('department_name')
    employee.department_id = temp.split(' - ', 2)[0]

    employee.title = request.form.get('title')
    employee.emp_number = request.form.get('emp_number')
    employee.address = request.form.get('address')
    employee.phone = request.form.get('phone')
    employee.wage = request.form.get('wage')
    employee.is_active = 'is_active' in request.form

    try:
        db.session.commit()
        flash(
            f'Employee {employee_id} was successfully updated!',
            'success')
    except Exception:
        import sys
        type, value, traceback = sys.exc_info()
        db.session.rollback()
        flash(f'An error occurred. Employee {employee_id} \
            could not be updated!', 'danger')
    finally:
        db.session.close()

    return make_response(redirect(url_for(
        'employees',
        data=db.session.query(Employee).order_by(
            Employee.department_id, Employee.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])))


# ----------------------------------------------------------------
# Products
# ----------------------------------------------------------------

@app.route('/products', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:product')
def products(self):
    # -------------------------
    # List all products
    # -------------------------

    dtos = []

    results = db.session.query(
            Product, Department, AisleContains, Aisle).filter(
            Product.department_id == Department.id).filter(
            Product.id == AisleContains.product_id).filter(
            AisleContains.aisle_number == Aisle.aisle_number).order_by(
                Product.id).all()

    for prod, dept, aico, aisl in results:
        dto = ProductDto(
            id=prod.id,
            name=prod.name,
            price_per_cost_unit=prod.price_per_cost_unit,
            cost_unit=prod.cost_unit,
            department_id=prod.department_id,
            quantity_in_stock=prod.quantity_in_stock,
            brand=prod.brand,
            production_date=prod.production_date,
            best_before_date=prod.best_before_date,
            plu=prod.plu,
            upc=prod.upc,
            organic=prod.organic,
            cut=prod.cut,
            animal=prod.animal,
            department_name=dept.name,
            aisle_number=aico.aisle_number,
            aisle_name=aisl.name
        )

        dtos.append(dto)

    return render_template(
        'grocery/products.html', data=dtos,
        departments=db.session.query(
            Department).order_by(Department.id).all(),
        aisles=db.session.query(Aisle).order_by(Aisle.aisle_number).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/products/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:product')
def add_product(self):
    # -------------------------
    # Add a product
    # -------------------------
    name = request.form.get('name', '')
    price_per_cost_unit = request.form.get('price_per_cost_unit', 0)
    cost_unit = request.form.get('cost_unit', '')
    department = request.form.get('department_name', '')
    department_id = department.split(' - ', 2)[0]
    quantity_in_stock = request.form.get('quantity_in_stock', 0)
    brand = request.form.get('brand', None)

    production_date = request.form.get(
        'production_date', datetime.today().strftime('%m/%d/%Y'))

    best_before_date = request.form.get(
        'best_before_date', datetime.today().strftime('%m/%d/%Y'))

    plu = request.form.get('plu', None)
    upc = request.form.get('upc', None)
    form_organic = request.form.get('organic', 0)
    cut = request.form.get('cut', None)
    animal = request.form.get('animal', None)
    aisle = request.form.get('aisle_name', '')
    aisle_number = aisle.split(' - ', 2)[0]

    max_id = db.session.query(func.max(Product.id)).one_or_none()
    id = max_id[0] + 1

    organic = 0

    if form_organic == 'on':
        organic = 1

    product = Product(
        id=id,
        name=name,
        price_per_cost_unit=price_per_cost_unit,
        cost_unit=cost_unit,
        department_id=department_id,
        quantity_in_stock=quantity_in_stock,
        brand=brand,
        production_date=production_date,
        best_before_date=best_before_date,
        plu=plu,
        upc=upc,
        organic=organic,
        cut=cut,
        animal=animal
    )

    try:
        db.session.add(product)
        db.session.commit()

        # Adding product to aisle after the product is added to the database
        # because of the product_id
        if aisle is not None:
            aisleContains = AisleContains(
                aisle_number=aisle_number,
                product_id=id
            )

            db.session.add(aisleContains)
            db.session.commit()

        flash(f'Product {name} was successfully added!', 'success')
    except Exception:
        import sys
        type, value, traceback = sys.exc_info()
        db.session.rollback()
        flash(
            f'An error occurred. Product {name} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'products',
        data=db.session.query(Product).order_by(Product.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))


@app.route('/products/<int:product_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:product')
def update_product(self, product_id):
    # -------------------------
    # Update data of product
    # -------------------------
    if request.form.get('_method') != 'PUT':
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)

    product = db.session.query(Product).filter(
        Product.id == product_id).one_or_none()

    if product is None:
        flash(
            f'No data with Product ID = {product_id} could be found!',
            'danger')
        abort(422)

    product.id = product_id
    product.name = request.form.get('name', '')
    product.price_per_cost_unit = request.form.get(
        'price_per_cost_unit', 0)
    product.cost_unit = request.form.get('cost_unit', '')
    product.quantity_in_stock = request.form.get('quantity_in_stock', 0)
    product.brand = request.form.get('brand', None)

    product.production_date = request.form.get(
        'production_date', datetime.today().strftime("%m/%d/%Y"))

    product.best_before_date = request.form.get(
        'best_before_date', datetime.today().strftime("%m/%d/%Y"))

    product.plu = request.form.get('plu', None)
    product.upc = request.form.get('upc', None)
    form_organic = request.form.get('organic', 0)

    product.organic = 0

    if form_organic == 'on':
        product.organic = 1

    product.cut = request.form.get('cut', None)
    product.animal = request.form.get('animal', None)

    department = request.form.get('department_name', '')
    product.department_id = department.split(' - ', 2)[0]

    # Need to update aisle_number in AisleContains table as well
    aisle = request.form.get('aisle_name', '')

    if aisle is not None:
        aisle_number = aisle.split(' - ', 2)[0]
        aisle_contains = db.session.query(AisleContains).filter(
            AisleContains.product_id == product_id).one_or_none()

        aisle_contains.aisle_number = aisle_number

    try:
        db.session.commit()
        flash(
            f'Product {product_id} was successfully updated!',
            'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Product {product_id} could not be updated!',
            'danger')
    finally:
        db.session.close()

    return make_response(redirect(url_for(
        'products',
        data=db.session.query(Product).order_by(Product.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])))


# ----------------------------------------------------------------
# Suppliers
# ----------------------------------------------------------------

@app.route('/suppliers', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:supplier')
def suppliers(self):
    # -------------------------
    # List all suppliers
    # -------------------------
    suppliers = db.session.query(Supplier).order_by(Supplier.id).all()

    return render_template(
        'grocery/suppliers.html', data=suppliers,
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/suppliers/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:supplier')
def add_supplier(self):
    # -------------------------
    # Add a supplier
    # -------------------------
    name = request.form.get('name', '')
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')

    max_id = db.session.query(func.max(Supplier.id)).one_or_none()
    id = max_id[0] + 1

    supplier = Supplier(
        id=id,
        name=name,
        address=address,
        phone=phone
    )

    try:
        db.session.add(supplier)
        db.session.commit()
        flash(
            f'Supplier {name} was successfully added!', 'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Supplier {name} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'suppliers',
        data=db.session.query(Supplier).order_by(Supplier.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))


@app.route('/suppliers/<int:supplier_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:supplier')
def update_supplier(self, supplier_id):
    # -------------------------
    # Update data of supplier
    # -------------------------
    if request.form.get('_method') != 'PUT':
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)

    supplier = db.session.query(Supplier).filter(
        Supplier.id == supplier_id).one_or_none()

    if supplier is None:
        flash(
            f'No data with Supplier id = {supplier_id} could be found!',
            'danger')
        abort(422)

    supplier.id = supplier_id
    supplier.name = request.form.get("name", "")
    supplier.address = request.form.get("address", "")
    supplier.phone = request.form.get("phone", "")

    try:
        db.session.commit()
        flash(f'Supplier {supplier_id} was successfully updated!', 'success')
    except Exception:
        db.session.rollback()
        flash(f'An error occurred. Supplier {supplier_id} \
            could not be updated!', 'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'suppliers',
        data=db.session.query(Supplier).order_by(Supplier.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))

# ----------------------------------------------------------------
# Purchases
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# TODO Can be designed better
# ----------------------------------------------------------------


@app.route('/suppliers', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:purchase')
def purchases(self):
    # -------------------------
    # List all orders
    # -------------------------
    purchases = Purchase.query.all()

    return render_template(
        'grocery/purchases.html', data=purchases,
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])


@app.route('/purchases/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:purchase')
def add_order(self):
    # -------------------------
    # Add an order
    # -------------------------
    product_name = request.form.get('product', '')
    quantity = request.form.get('quantity', 0)
    customer_name = request.form.get('customer', '')

    purchase_date = request.form.get(
        'purchase_date', datetime.today().strftime('%m/%d/%Y'))

    total = request.form.get('total', 0)

    product = Product.query.filter(
        Product.name == product_name).one_or_none()
    customer = Customer.query.filter(
        Customer.name == customer_name).one_or_none()

    purchase = Purchase(
        product_id=product.id,
        quantity=quantity,
        customer_id=customer.id,
        purchase_date=purchase_date,
        total=total
    )

    try:
        db.session.add(purchase)
        db.session.commit()
        flash(
            f'Order {product.id} was successfully added!',
            'success')
    except Exception:
        db.session.rollback()
        flash(
            f'An error occurred. Order {product.id} could not be added!',
            'danger')
    finally:
        db.session.close()

    return redirect(url_for(
        'purchases',
        data=db.session.query(Purchase).order_by(Purchase.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key]))


@app.route('/purchases/<int:purchase_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:purchase')
def update_order(purchase_id):
    # -------------------------
    # Update data of order
    # -------------------------

    if request.form.get('_method') != 'PUT':
        flash(
            'Cannot perform this action. Please contact administrator',
            'danger')
        abort(405)

    purchase = Purchase.query.filter(
        Purchase.id == purchase_id).one_or_none()
    product_name = request.form.get('product', '')
    purchase.quantity = request.form.get('quantity', 0)
    customer_name = request.form.get('customer_id', '')

    purchase.purchase_date = request.form.get(
        'purchase_date', datetime.today().strftime('%m/%d/%Y'))

    purchase.total = request.form.get('total', 0)

    product = Product.query.filter(
        Product.name == product_name).one_or_none()
    customer = Customer.query.filter(
        Customer.name == customer_name).one_or_none()

    purchase.product_id = product.product_id
    purchase.customer_id = customer.customer_id

    if len(purchase) == 0:
        flash(
            f'No data with Supplier id = {purchase_id} could be found!',
            'danger')
        abort(422)

    try:
        db.session.commit()
        flash(
            f'Order {purchase_id} was successfully updated!',
            'success')
    except Exception:
        db.session.rollback()
        flash(f'An error occurred. Order {purchase_id} \
            could not be updated!', 'danger')
    finally:
        db.session.close()

    return make_response(redirect(url_for(
        'purchases',
        data=db.session.query(Purchase).order_by(Purchase.id).all(),
        userinfo=session[conf_profile_key],
        accessinfo=session[conf_access_key])))


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# -------------------------------------------------------
# Handling Exceptions
# -------------------------------------------------------


@app.errorhandler(422)
def unprocessable(error):
    return render_template(
        'errors/422.html',
        data=jsonify({
            'message': error.error.get("description"),
            'status_code': error.status_code
        })), 422


@app.errorhandler(400)
def bad_request(error):
    return render_template(
        'errors/400.html',
        data=jsonify({
            'message': error.error.get("description"),
            'status_code': error.status_code
        })), 400


@app.errorhandler(401)
def unauthorized(error):
    return render_template(
        'errors/401.html',
        data=jsonify({
            'message': error.error.get("description"),
            'status_code': error.status_code
        })), 401


@app.errorhandler(403)
def forbidden(error):
    return render_template(
        'errors/403.html',
        data=jsonify({
            'message': error.error.get("description"),
            'status_code': error.status_code
        })), 403


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template(
        'errors/405.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 405


@app.errorhandler(500)
def server_error(error):
    return render_template(
        'errors/500.html',
        data=jsonify({
            'message': error.error.get("description"),
            'status_code': error.status_code
        })), 500


@app.errorhandler(404)
def resource_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return render_template('errors/errors.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
