from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    flash,
    render_template,
    abort,
    jsonify)
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import (
    CORS,
    cross_origin)
import dateutil.parser
import babel
import logging
import sys
from logging import (
    FileHandler,
    Formatter)
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

# Local imports...
from config import Config
from models import (
    Aisle,
    Product,
    Customer,
    Purchase,
    Department,
    Employee,
    Supplier,
    AisleContains,
    EmployeeDto,
    ProductDto,
    setup_db)
from exceptions import (
    AuthError,
    EmptyEntityError)
from auth import (
    auth_bp,
    requires_auth,
    requires_login)

app = Flask(__name__)

###########################################################
#
# CONSTANTS
#
###########################################################

app.config.from_object(Config)

conf_profile_key = app.config['PROFILE_KEY']
conf_access_key = app.config['ACCESS_KEY']
jwt_payload = app.config['JWT_PAYLOAD']
id_key = app.config['ID_KEY']
profile_key = app.config['PROFILE_KEY']
test_token = app.config['TEST_TOKEN']

audience = app.config['API_AUDIENCE']
auth0_domain = app.config['AUTH0_DOMAIN']
algorithms = app.config['ALGORITHMS']
client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET']
access_token_url = app.config['ACCESS_TOKEN_URL']
authorize_url = app.config['AUTHORIZE_URL']
callback_uri = app.config['CALLBACK_URL']
secret_key = app.config['SECRET_KEY']

conf = Config()

if app.config["SQLALCHEMY_DATABASE_URI"] is None:
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        conf.SQLALCHEMY_DATABASE_URI

if app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is None:
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = \
        conf.SQLALCHEMY_TRACK_MODIFICATIONS

###########################################################
#
# LOGGING
#
###########################################################

if not app.debug:
    formatter = Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('LOGGING LEVEL: INFO')


###########################################################
#
# MAIN APP CODE
#
###########################################################


setup_db(app)

CORS(app, resources={'/': {'origins': '*'}})

app.secret_key = secret_key

# ---------------------------------------------------------------------------
# TODO Pagination code for displaying database items
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

with app.app_context():
    swagger_bp = get_swaggerui_blueprint(
        app.config['SWAGGER_URL'],
        app.config['API_URL'],
        config={
            'app_name': "UdaciMarket_Management_System"
        }
    )

    app.register_blueprint(swagger_bp, url_prefix='/swagger')
    app.register_blueprint(auth_bp)


###########################################################
#
# AUTHORIZATION & AUTHENTICATION
#
###########################################################

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=client_id,
    client_secret=client_secret,
    api_base_url=f'https://{auth0_domain}',
    access_token_url=access_token_url,
    authorize_url=authorize_url,
    client_kwargs={
        'scope': 'openid profile email'
    },
)


###########################################################
#
# ROUTES
#
###########################################################

'''
Authorization and Authentication Routes
'''


@app.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=callback_uri,
        audience=audience)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for(
        'home', _external=True),
        'client_id': client_id}
    return redirect(f'{auth0.api_base_url}/v2/logout?{urlencode(params)}')


@app.route('/callback')
def callback_handling():
    token = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[jwt_payload] = userinfo
    session[conf_profile_key] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture'],
        'nickname': userinfo['nickname']
    }
    session[id_key] = {'id': token['id_token']}
    session[conf_access_key] = \
        {'access': token['access_token']}

    return render_template(
        'grocery/home.html',
        nickname=session[conf_profile_key]['nickname'] if
        'POSTMAN_TOKEN' not in request.headers else 'Guest')


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


@app.route('/')
@app.route('/home')
def home():
    # -------------------
    # Home page
    # -------------------
    try:
        return render_template(
            'grocery/home.html',
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers else 'Guest')
    except KeyError as e:
        tb = sys.exc_info()
        app.logger.info(e.with_traceback(tb[2]))
        return render_template('grocery/home.html')


@app.route('/constructions')
def constructions():
    # -------------------
    # Construction page
    # -------------------
    return render_template('errors/construction.html')


@app.route('/swaggerLink')
@requires_login
def swagger_link():
    # -------------------
    # Swagger page
    # -------------------
    return redirect('/swagger')


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
    try:
        aisles = Aisle().list_all_aisles()

        if aisles is None:
            app.logger.info('Aisles table is empty?')
            abort(422)

        return render_template(
            'grocery/aisles.html', data=aisles,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException:
        app.logger.info('An error occurred. Aisles not available')
        abort(422)


@app.route('/aisles/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:aisle')
def add_aisle(self):
    # -------------------------
    # Add an aisle
    # -------------------------
    aisle_number = request.form.get('aisle_number', '')
    name = request.form.get('name', '')

    aisle = Aisle(
        aisle_number=aisle_number,
        name=name)

    try:
        aisle.add_aisle_to_database()

        flash(
            f'Aisle {aisle.aisle_number} was successfully added!',
            'success')
    except EmptyEntityError as e:
        app.logger.info(f'{e.description} - Aisle')
        abort(422)
    except BaseException as e:
        tb = sys.exc_info()
        app.logger.info(e.with_traceback(tb[2]))
        app.logger.info(
            f'An error occurred. Aisle {aisle.aisle_number} \
            could not be added!')
        abort(422)

    return redirect(url_for('aisles'))


@app.route(
    '/aisles/<string:aisle_number>', methods=['PUT', 'DELETE', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth(['delete:aisle', 'put:aisle'])
def handle_aisle(self, aisle_number):
    aisle = Aisle(aisle_number=aisle_number)

    try:
        aisle = aisle.list_one_or_none_aisle()

        if aisle is None:
            app.logger.info(
                f'No data with Aisle number = {aisle_number} could be found!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'No data with Aisle number = {aisle_number} could be found!')
        abort(422)

    if request.method == 'DELETE':
        # -------------------------
        # Delete an aisle
        # -------------------------

        aisle_contains = AisleContains(
            aisle_number=aisle_number,
            product_id=0
        )

        try:
            aisle_contains_list = \
                aisle_contains.list_all_aisle_contains_filtered()

            # Before deleting the aisle, the records in the aisle_contains
            # table needs to be deleted first to uphold referential integrity
            if aisle_contains_list is not None and \
                    len(aisle_contains_list) > 0:
                aisle_contains = \
                    aisle_contains.delete_aisle_contains_from_database(
                        aisle_contains_list)

            aisle = aisle.delete_aisle_from_database()

            flash(f'Aisle {aisle_number} was successfully deleted!', 'success')
        except BaseException:
            app.logger.info(
                f'An error occurred. Aisle {aisle_number} was failed \
                    to be deleted!')
            abort(422)

    elif request.form.get('_method') == 'PUT':
        # -------------------------
        # Update data of aisle
        # -------------------------

        aisle.aisle_number = aisle_number

        # TODO Actually I think the correct thing to do is to check whether
        # the new value is different than the old value first, then
        # replace if they are different and remain if they are the same.
        # What I did here is okay except for the fact that when user is
        # trying to delete an entry... s/he can't
        aisle.name = request.form.get('name', aisle.name)

        try:
            aisle = aisle.update_aisle_in_database()
            flash(
                f'Aisle {aisle_number} was successfully updated!',
                'success')
        except BaseException:
            app.logger.info(
                f'An error occurred. Aisle {aisle_number} \
                could not be updated!')
            abort(422)
    else:
        app.logger.info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    return redirect(url_for('aisles'))

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
    try:
        customers = Customer().list_all_customers()

        if customers is None:
            app.logger.info('Customers table is empty?')
            abort(422)

        return render_template(
            'grocery/customers.html', data=customers,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException:
        app.logger.info('An error occurred. Customers not available')
        abort(422)


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

    id = 0

    try:
        id = Customer().get_next_customer_id()
    except BaseException:
        app.logger.info('Error finding next customer ID')
        abort(422)

    customer = Customer(
        id=id,
        name=name,
        phone=phone,
        email=email
    )

    try:
        customer = customer.add_customer_to_database()
        flash(f'Customer {name} was successfully added!', 'success')
    except BaseException:
        app.logger.info(
            f'An error occurred. Customer {name} could not be added!')
        abort(422)

    return redirect(url_for('customers'))


@app.route('/customers/<string:customer_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:customer')
def update_customer(self, customer_id):
    # -------------------------
    # Update data of customer
    # -------------------------
    if request.form.get('_method') != 'PUT':
        app.logger.Info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    customer = Customer(id=customer_id)

    try:
        customer = customer.list_one_or_none_customer()

        if customer is None:
            app.logger.info(
                f'No data with Customer ID = {customer_id} could be found!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'An error occurred. No data with Customer ID\
                 = {customer_id} could be found!')
        abort(422)

    customer.id = customer_id
    customer.name = request.form.get('name', customer.name)
    customer.phone = request.form.get('phone', customer.phone)
    customer.email = request.form.get('email', customer.email)

    try:
        customer.update_customer_in_database()
        flash(
            f'Customer {customer_id} was successfully updated!',
            'success')
    except BaseException:
        app.log.info(f'An error occurred. Customer {customer_id} \
            could not be updated!')
        abort(422)

    return redirect(url_for('customers'))


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
    try:
        departments = Department().list_all_departments()

        if departments is None:
            app.logger.info('Departments table is empty?')
            abort(422)

        return render_template(
            'grocery/departments.html', data=departments,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException:
        app.logger.info('An error occurred. Departments not available')
        abort(422)


@app.route('/departments/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:department')
def add_department(self):
    # -------------------------
    # Add a department
    # -------------------------
    name = request.form.get('name', '')

    id = 0

    try:
        id = Department().get_next_department_id()
    except BaseException:
        app.logger.info('Error finding next department ID')
        abort(422)

    department = Department(
        id=id,
        name=name
    )

    try:
        department = department.add_department_to_database()
        flash(f'Department {name} was successfully added!', 'success')
    except BaseException:
        app.logger.info(
            f'An error occurred. Department {name} could not be added!')
        abort(422)

    return redirect(url_for('departments'))


@app.route('/departments/<string:department_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:department')
def update_department(self, department_id):
    # -------------------------
    # Update data of department
    # -------------------------
    if request.form.get('_method') != 'PUT':
        app.logger.Info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    department = Department(id=department_id)

    try:
        department = department.list_one_or_none_department()

        if department is None:
            app.logger.info(
                f'No data with Department ID =\
                    {department_id} could be found!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'An error occurred. No data with Department ID\
                 = {department_id} could be found!')
        abort(422)

    department.id = department_id
    department.name = request.form.get('name', department.name)

    try:
        department.update_department_in_database()
        flash(
            f'Department {department_id} was successfully updated!',
            'success')
    except BaseException:
        app.log.info(f'An error occurred. Department {department_id} \
            could not be updated!')
        abort(422)

    return redirect(url_for('departments'))


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
    try:
        results = Employee().list_all_employees_filtered(Department())

        if results is None:
            app.logger.info('No matches between Employees\
                and Department tables')
            abort(422)

        dtos = []

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

        departments = Department().list_all_departments()

        if departments is None or len(departments) == 0:
            app.logger.info('Departments table is empty?')
            abort(422)

        return render_template(
            'grocery/employees.html', data=dtos,
            departments=departments,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException:
        app.logger.info('An error occurred. Employees not available')
        abort(422)


@app.route('/employees/create', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('post:employee')
def add_employee(self):
    # -------------------------
    # Add an employee
    # -------------------------
    name = request.form.get('name', '')
    department = request.form.get('department_name', '')
    department_id = int(department.split(' - ', 2)[0])
    title = request.form.get('title', '')
    emp_number = int(request.form.get('emp_number', ''))
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    wage = request.form.get('wage', '')

    id = 0

    try:
        id = Employee().get_next_employee_id()
    except BaseException:
        app.logger.info('Error finding next employee ID')
        abort(422)

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
        employee = employee.add_employee_to_database()
        flash(f'Employee {name} was successfully added!', 'success')
    except BaseException:
        app.logger.info(
            f'An error occurred. Employee {name} could not be added!')
        abort(422)

    return redirect(url_for('employees'))


@app.route('/employees/<string:employee_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:employee')
def update_employee(self, employee_id):
    # -------------------------
    # Update data of employee
    # -------------------------
    if request.form.get('_method') != 'PUT':
        app.logger.Info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    employee = Employee(id=employee_id)

    try:
        employee = employee.list_one_or_none_employee()

        if employee is None:
            app.logger.info(
                f'No data with Employee ID = {employee_id} could be found!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'An error occurred. No data with Employee ID\
                 = {employee_id} could be found!')
        abort(422)

    employee.id = employee_id
    employee.name = request.form.get('name', employee.name)

    temp = request.form.get('department_name')
    employee.department_id = temp.split(' - ', 2)[0]

    employee.title = request.form.get('title', employee.title)
    employee.emp_number = request.form.get('emp_number', employee.emp_number)
    employee.address = request.form.get('address', employee.address)
    employee.phone = request.form.get('phone', employee.phone)
    employee.wage = request.form.get('wage', employee.wage)
    employee.is_active = 'is_active' in request.form

    try:
        employee.update_employee_in_database()
        flash(
            f'Employee {employee_id} was successfully updated!',
            'success')
    except BaseException:
        app.log.info(f'An error occurred. Employee {employee_id} \
            could not be updated!')
        abort(422)

    return redirect(url_for('employees'))


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
    try:
        results = Product().list_all_products_filtered(
            Department(), AisleContains(), Aisle())

        if results is None:
            app.logger.info('No matches between Products,\
                Departments, AisleContains, and Aisles tables')
            abort(422)

        dtos = []

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

        departments = Department().list_all_departments()

        if departments is None or len(departments) == 0:
            app.logger.info('Departments table is empty?')
            abort(422)

        aisles = Aisle().list_all_aisles()

        if aisles is None or len(aisles) == 0:
            app.logger.info('Aisles table is empty?')
            abort(422)

        return render_template(
            'grocery/products.html', data=dtos,
            departments=departments, aisles=aisles,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException as e:
        tb = sys.exc_info()
        app.logger.info(e.with_traceback(tb[2]))
        app.logger.info('An error occurred. Products not available')
        abort(422)


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

    id = 0

    try:
        id = Product().get_next_product_id()
    except BaseException:
        app.logger.info('Error finding next product ID')
        abort(422)

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
        product = product.add_product_to_database()

        # Adding product to aisle after the product is added to the database
        # because of the product_id
        if aisle is not None:
            aisle_contains = AisleContains(
                aisle_number=aisle_number,
                product_id=id
            )

            aisle_contains = aisle_contains.add_aisle_contains_to_database()

        flash(f'Product {name} was successfully added!', 'success')
    except BaseException:
        app.logger.info(
            f'An error occurred. Product {name} could not be added!')
        abort(422)

    return redirect('/products')


@app.route('/products/<int:product_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:product')
def update_product(self, product_id):
    # -------------------------
    # Update data of product
    # -------------------------
    if request.form.get('_method') != 'PUT':
        app.logger.Info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    product = Product(id=product_id)

    try:
        product = product.list_one_or_none_product()

        if product is None:
            app.logger.info(
                f'No data with Employee ID = {product_id} could be found!')
            abort(422)

        product.id = product_id
        product.name = request.form.get('name', product.name)
        product.price_per_cost_unit = request.form.get(
            'price_per_cost_unit', product.price_per_cost_unit)
        product.cost_unit = request.form.get('cost_unit', product.cost_unit)
        product.quantity_in_stock = request.form.get(
            'quantity_in_stock', product.quantity_in_stock)
        product.brand = request.form.get('brand', product.brand)

        product.production_date = request.form.get(
            'production_date', product.production_date)

        product.best_before_date = request.form.get(
            'best_before_date', product.best_before_date)

        product.plu = request.form.get('plu', product.plu)
        product.upc = request.form.get('upc', product.upc)
        form_organic = request.form.get('organic', 'off')

        product.organic = 0

        if form_organic == 'on':
            product.organic = 1

        product.cut = request.form.get('cut', product.cut)
        product.animal = request.form.get('animal', product.animal)

        department = request.form.get('department_name')
        product.department_id = department.split(' - ', 2)[0]

        # Need to update aisle_number in AisleContains table as well
        aisle = request.form.get('aisle_name')

        if aisle is not None:
            aisle_number = int(aisle.split(' - ', 2)[0])
            aisle_contains = AisleContains(
                aisle_number=aisle_number,
                product_id=product_id
            )

            aisle_contains = \
                aisle_contains.list_one_or_none_aisle_contains(product)

            if aisle_contains is not None:
                aisle_contains.aisle_number = aisle_number
            else:
                aisle_contains = AisleContains(
                    aisle_number=aisle_number,
                    product_id=product_id
                )

                # If the product is associated with any aisle, this code
                # should never have been reached. The other option here
                # would be to add the association to the AisleContains
                # table.
                try:
                    aisle_contains = \
                        aisle_contains.add_aisle_contains_to_database()
                except BaseException:
                    app.logger.info(
                        f'An error occurred. Product {product_id} failed to be \
                        associated with Aisle {aisle_number}.')
                    abort(422)

        try:
            product.update_product_in_database()
            flash(
                f'Product {product_id} was successfully updated!',
                'success')
        except BaseException:
            app.logger.info(
                f'An error occurred. Product {product_id} \
                    could not be updated!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'An error occurred. No data with Product ID\
                 = {product_id} could be found!')
        abort(422)

    return redirect('/products')


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
    try:
        suppliers = Supplier().list_all_suppliers()

        if suppliers is None:
            app.logger.info('Suppliers table is empty?')
            abort(422)

        return render_template(
            'grocery/suppliers.html', data=suppliers,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException:
        app.logger.info('An error occurred. Suppliers not available')
        abort(422)


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

    id = 0

    try:
        id = Supplier().get_next_supplier_id()
    except BaseException:
        app.logger.info('Error finding next supplier ID')
        abort(422)

    supplier = Supplier(
        id=id,
        name=name,
        address=address,
        phone=phone
    )

    try:
        supplier = supplier.add_supplier_to_database()
        flash(f'Supplier {name} was successfully added!', 'success')
    except BaseException:
        app.logger.info(
            f'An error occurred. Supplier {name} could not be added!')
        abort(422)

    return redirect(url_for('suppliers'))


@app.route('/suppliers/<int:supplier_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:supplier')
def update_supplier(self, supplier_id):
    # -------------------------
    # Update data of supplier
    # -------------------------
    if request.form.get('_method') != 'PUT':
        app.logger.Info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    supplier = Supplier(id=supplier_id)

    try:
        supplier = supplier.list_one_or_none_supplier()

        if supplier_id is None:
            app.logger.info(
                f'No data with Supplier ID =\
                    {supplier_id} could be found!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'An error occurred. No data with Supplier ID\
                 = {supplier_id} could be found!')
        abort(422)

    supplier.id = supplier_id
    supplier.name = request.form.get("name", supplier.name)
    supplier.address = request.form.get("address", supplier.address)
    supplier.phone = request.form.get("phone", supplier.phone)

    try:
        supplier.update_supplier_in_database()
        flash(
            f'Supplier {supplier_id} was successfully updated!',
            'success')
    except BaseException:
        app.log.info(f'An error occurred. Supplier {supplier_id} \
            could not be updated!')
        abort(422)

    return redirect(url_for('suppliers'))


# ----------------------------------------------------------------
# Purchases
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# TODO Can be designed better
# ----------------------------------------------------------------


@app.route('/purchases', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('get:purchase')
def purchases(self):
    # -------------------------
    # List all orders
    # -------------------------
    try:
        purchases = Purchase().list_all_purchases()

        if purchases is None:
            app.logger.info('Purchases table is empty?')
            abort(422)

        return render_template(
            'grocery/purchases.html', data=purchases,
            nickname=session[conf_profile_key]['nickname'] if
            'POSTMAN_TOKEN' not in request.headers and
            'test_permission' not in request.headers else 'Guest')
    except BaseException:
        app.logger.info('An error occurred. Suppliers not available')
        abort(422)


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
        purchase = purchase.add_purchase_to_database()
        flash(
            f'Product ID {product.id} was successfully added \
            to purchases table!')
    except BaseException:
        app.logger.info(
            f'An error occurred. Product ID {product.id} could not be added!')
        abort(422)

    return redirect(url_for('purchases'))


@app.route('/purchases/<int:purchase_id>', methods=['PUT', 'POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('put:purchase')
def update_order(purchase_id):
    # -------------------------
    # Update data of order
    # -------------------------
    if request.form.get('_method') != 'PUT':
        app.logger.Info(
            'Cannot perform this action. Please contact administrator')
        abort(405)

    purchase = Purchase(id=purchase_id)

    try:
        purchase = purchase.list_one_or_none_purchase()

        if purchase_id is None:
            app.logger.info(
                f'No data with Purchase ID =\
                    {purchase_id} could be found!')
            abort(422)
    except BaseException:
        app.logger.info(
            f'An error occurred. No data with Purchase ID\
                 = {purchase_id} could be found!')
        abort(422)

    purchase.id = purchase_id
    product_name = request.form.get('product')
    purchase.quantity = request.form.get('quantity', purchase.quantity)
    customer_name = request.form.get('customer_id')

    purchase.purchase_date = request.form.get(
        'purchase_date', purchase.purchase_date)

    purchase.total = request.form.get('total', purchase.total)

    product = Product.query.filter(
        Product.name == product_name).one_or_none()
    customer = Customer.query.filter(
        Customer.name == customer_name).one_or_none()

    purchase.product_id = product.product_id
    purchase.customer_id = customer.customer_id

    try:
        purchase.update_purchase_in_database()
        flash(
            f'Purchase {purchase_id} was successfully updated!',
            'success')
    except BaseException:
        app.log.info(f'An error occurred. Purchase {purchase_id} \
            could not be updated!')
        abort(422)

    return redirect(url_for('purchases'))


###########################################################
#
# EXCEPTION HANDLERS
#
###########################################################


@app.errorhandler(422)
def unprocessable(error):
    app.logger.info('ErrorHandler 422 called')
    return render_template(
        'errors/422.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 422


@app.errorhandler(400)
def bad_request(error):
    app.logger.info('ErrorHandler 400 called')
    return render_template(
        'errors/400.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 400


@app.errorhandler(401)
def unauthorized(error):
    app.logger.info('ErrorHandler 401 called')
    return render_template(
        'errors/401.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 401


@app.errorhandler(403)
def forbidden(error):
    app.logger.info('ErrorHandler 403 called')
    return render_template(
        'errors/403.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 403


@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.info('ErrorHandler 405 called')
    return render_template(
        'errors/405.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 405


@app.errorhandler(500)
def server_error(error):
    app.logger.info('ErrorHandler 500 called')
    return render_template(
        'errors/500.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 500


@app.errorhandler(404)
def resource_not_found(error):
    app.logger.info('ErrorHandler 404 called')
    return render_template(
        'errors/404.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        })), 404


@app.errorhandler(AuthError)
def auth_error(error):
    app.logger.info('ErrorHandler AuthError called')
    return render_template(
        'errors/errors.html',
        data=jsonify({
            'message': error.description,
            'status_code': error.code
        }))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
