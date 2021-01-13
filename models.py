import sys
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    text)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func

# Local imports...
from exceptions import EmptyEntityError


Base = declarative_base()
metadata = Base.metadata

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


class Aisle(Base):
    __tablename__ = 'aisles'

    aisle_number = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    products = relationship('Product', secondary='aislecontains')

    def __init__(self, aisle_number=0, name=None):
        self.aisle_number = aisle_number
        self.name = name

    def list_all_aisles(self):
        data = None
        try:
            data = _list_all_data(db, Aisle())
        except BaseException:
            raise

        return data

    def list_one_or_none_aisle(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_aisle_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_aisle_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def delete_aisle_from_database(self):
        try:
            _delete_entity(db, entity=self)
        except EmptyEntityError:
            raise
        except BaseException:
            raise

        return self

    def __repr__(self):
        return f'Aisle("{self.aisle_number}","{self.name}")'


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('customers_id_seq'::regclass)"))
    name = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))

    def __init__(self, id=0, name=None, phone=None, email=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def list_all_customers(self):
        data = None
        try:
            data = _list_all_data(db, Customer())
        except BaseException:
            raise

        return data

    def list_one_or_none_customer(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_customer_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_customer_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def get_next_customer_id(self):
        id = 0

        try:
            id = _get_next_id(db, Customer())
        except BaseException:
            raise

        return id

    def __repr__(self):
        return f'Customer("{self.id}","{self.name}",\
            "{self.phone}","{self.email}")'


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('departments_id_seq'::regclass)"))
    name = Column(String(255))

    def __init__(self, id=0, name=None):
        self.id = id
        self.name = name

    def list_all_departments(self):
        data = None
        try:
            data = _list_all_data(db, Department())
        except BaseException:
            raise

        return data

    def list_one_or_none_department(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_department_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_department_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def get_next_department_id(self):
        id = 0

        try:
            id = _get_next_id(db, Department())
        except BaseException:
            raise

        return id

    def __repr__(self):
        return f'Department("{self.id}","{self.name}")'


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('suppliers_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    phone = Column(String(255), nullable=False)

    def __init__(self, id=0, name=None, address=None, phone=None):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone

    def list_all_suppliers(self):
        data = None
        try:
            data = _list_all_data(db, Supplier())
        except BaseException:
            raise

        return data

    def list_one_or_none_supplier(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_supplier_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_supplier_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def get_next_supplier_id(self):
        id = 0

        try:
            id = _get_next_id(db, Supplier())
        except BaseException:
            raise

        return id

    def __repr__(self):
        return f'Supplier("{self.id}","{self.name}",\
            "{self.address}","{self.phone}")'


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('employees_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    department_id = Column(ForeignKey('departments.id'))
    title = Column(String(255))
    emp_number = Column(BigInteger, nullable=False)
    address = Column(String(255))
    phone = Column(String(255))
    wage = Column(Integer)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))

    department = relationship('Department')

    def __init__(
            self, id=0, name=None, department_id=0, title=None,
            emp_number=0, address=None, phone=None, wage=0,
            is_active=False):
        self.id = id,
        self.name = name,
        self.department_id = department_id,
        self.title = title,
        self.emp_number = emp_number,
        self.address = address,
        self.phone = phone,
        self.wage = wage,
        self.is_active = is_active

    def list_all_employees(self, entity=None):
        data = None
        try:
            data = _list_all_data(db, Employee(), entity)
        except BaseException:
            raise

        return data

    def list_all_employees_filtered(self, entity2=None):
        data = None
        try:
            data = _list_all_data_filtered(
                db, entity=Employee(), entity2=Department())
        except BaseException:
            raise

        return data

    def list_one_or_none_employee(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_employee_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_employee_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def get_next_employee_id(self):
        id = 0

        try:
            id = _get_next_id(db, Employee())
        except BaseException:
            raise

        return id

    def __repr__(self):
        return f'Employee("{self.id}","{self.name}",\
            "{self.department_id}","{self.title}",\
            "{self.emp_number}","{self.address}",\
            "{self.phone}","{self.wage}","{self.is_active}")'


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('products_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    price_per_cost_unit = Column(Float(53), nullable=False)
    cost_unit = Column(String(255), nullable=False)
    department_id = Column(ForeignKey('departments.id'), nullable=False)
    quantity_in_stock = Column(Integer)
    brand = Column(String(255))
    production_date = Column(Date)
    best_before_date = Column(Date)
    plu = Column(Integer)
    upc = Column(BigInteger)
    organic = Column(Integer)
    cut = Column(String(255))
    animal = Column(String(255))

    department = relationship('Department')
    suppliers = relationship('Supplier', secondary='providedby')

    def __init__(
            self, id=0, name=None, price_per_cost_unit=0, cost_unit=None,
            department_id=0, quantity_in_stock=0, brand=None,
            production_date=None, best_before_date=None, plu=0,
            upc=0, organic=0, cut=None, animal=None):
        self.id = id
        self.name = name,
        self.price_per_cost_unit = price_per_cost_unit,
        self.cost_unit = cost_unit,
        self.department_id = department_id,
        self.quantity_in_stock = quantity_in_stock,
        self.brand = brand,
        self.production_date = production_date,
        self.best_before_date = best_before_date,
        self.plu = plu,
        self.upc = upc,
        self.organic = organic,
        self.cut = cut,
        self.animal = animal

    def list_all_products(self):
        data = None

        try:
            data = _list_all_data(db, self)
        except BaseException:
            raise

        return data

    def list_all_products_filtered(
            self, entity2=None, entity3=None, entity4=None):
        data = None

        try:
            data = _list_all_data_filtered(
                db, self, Department(), AisleContains(), Aisle())
        except BaseException:
            raise

        return data

    def list_one_or_none_product(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_product_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_product_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def get_next_product_id(self):
        id = 0

        try:
            id = _get_next_id(db, Product())
        except BaseException:
            raise

        return id

    def __repr__(self):
        return f'Product("{self.id}","{self.name}",\
            "{self.price_per_cost_unit}","{self.cost_unit}",\
            "{self.department_id}","{self.quantity_in_stock}",\
            "{self.brand}","{self.production_date}",\
            "{self.best_before_date}","{self.plu}",\
            "{self.upc}","{self.organic}","{self.cut}",\
            "{self.animal}")'


class Providesdelivery(Base):
    __tablename__ = 'providesdelivery'

    delivery_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('providesdelivery_delivery_id_seq'::regclass)"))
    supplier_id = Column(ForeignKey('suppliers.id'), nullable=False)

    supplier = relationship('Supplier')
    products = relationship('Product', secondary='receivedfrom')

    def __repr__(self):
        return f'Providesdelivery("{self.delivery_id}","{self.supplier_id}")'


t_aislecontains = Table(
    'aislecontains', metadata,
    Column('aisle_number', ForeignKey(
        'aisles.aisle_number'), primary_key=True, nullable=False),
    Column('product_id', ForeignKey(
        'products.id'), primary_key=True, nullable=False)
)


class AisleContains(Base):
    __table__ = t_aislecontains

    def __init__(self, aisle_number=0, product_id=0):
        self.aisle_number = aisle_number
        self.product_id = product_id

    def list_all_aisle_contains_filtered(self):
        data = None
        try:
            data = _list_all_data_filtered(db, self)
        except BaseException:
            raise

        return data

    def list_one_or_none_aisle_contains(self, entity2=None):
        data = None
        try:
            data = _list_one_or_none_data(db, self, entity2)
        except BaseException:
            raise

        return data

    def add_aisle_contains_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

    def delete_aisle_contains_from_database(self, aisle_contains_list):
        try:
            _delete_entity(db, entity_list=aisle_contains_list)
        except EmptyEntityError:
            raise
        except BaseException:
            raise

        return aisle_contains_list


t_providedby = Table(
    'providedby', metadata,
    Column('product_id', ForeignKey(
        'products.id'), primary_key=True, nullable=False),
    Column('supplier_id', ForeignKey(
        'suppliers.id'), primary_key=True, nullable=False)
)


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, nullable=False, server_default=text(
        "nextval('purchases_id_seq'::regclass)"))
    product_id = Column(ForeignKey(
        'products.id'), primary_key=True, nullable=False)
    quantity = Column(Integer)
    customer_id = Column(ForeignKey('customers.id'))
    purchase_date = Column(Date)
    total = Column(Float(53))
    is_cancelled = Column(
        Boolean, nullable=False, server_default=text("false"))

    customer = relationship('Customer')
    product = relationship('Product')

    def __init__(
            self, id=0, product_id=0, quantity=0, customer_id=0,
            purchase_date=None, total=0, is_cancelled=False):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.customer_id = customer_id
        self.purchase_date = purchase_date
        self.total = total
        self.is_cancelled = is_cancelled

    def list_all_purchases(self):
        data = None
        try:
            data = _list_all_data(db, Purchase())
        except BaseException:
            raise

        return data

    def list_one_or_none_purchase(self):
        data = None

        try:
            data = _list_one_or_none_data(db, self)
        except BaseException:
            raise

        return data

    def add_purchase_to_database(self):
        try:
            _add_entity(db, self)
        except BaseException:
            raise

        return self

    def update_purchase_in_database(self):
        try:
            _update_entity(db)
        except BaseException:
            raise

        return self

    def get_next_purchase_id(self):
        id = 0

        try:
            id = _get_next_id(db, Purchase())
        except BaseException:
            raise

        return id

    def __repr__(self):
        return f'Purchase("{self.id}","{self.product_id}",\
            "{self.quantity}","{self.customer_id}",\
            "{self.purchase_date}","{self.total}",\
            "{self.is_cancelled}")'


t_receivedfrom = Table(
    'receivedfrom', metadata,
    Column('product_id', ForeignKey(
        'products.id'), primary_key=True, nullable=False),
    Column('delivery_id', ForeignKey(
        'providesdelivery.delivery_id'), primary_key=True, nullable=False)
)


class EmployeeDto(Employee):
    def __init__(
        self, department_name, id, name, department_id, title,
            emp_number, address, phone, wage, is_active):
        super().__init__(
            id, name, department_id, title,
            emp_number, address, phone, wage, is_active)
        self.department_name = department_name

        def __repr__(self):
            return f'EmployeeDto("{super.__repr__()}" and\
                "{self.department_name}")'


class ProductDto(Product):
    def __init__(
        self, department_name, id, name, price_per_cost_unit,
            cost_unit, department_id, quantity_in_stock, brand,
            production_date, best_before_date, plu, upc, organic, cut,
            animal, aisle_name, aisle_number):
        super().__init__(
            id, name, price_per_cost_unit,
            cost_unit, department_id, quantity_in_stock, brand,
            production_date, best_before_date, plu, upc, organic, cut,
            animal)
        self.department_name = department_name
        self.aisle_name = aisle_name
        self.aisle_number = aisle_number

        def __repr__(self):
            return f'ProductDto("{super.__repr__()}" and\
                "{self.department_name}","{self.aisle_nnumber}",\
                "{self.aisle_name}")'


###########################################################
#
# HELPER FUNCTIONS
#
###########################################################


def _list_all_data(db, entity) -> list:
    data = None
    model = type(entity)
    model_name = model.__name__

    session = db.session
    session.expire_on_commit = False

    try:
        if model_name == 'Employee':
            data = session.query(model).order_by(
                model.department_id, model.id).all()
        elif model_name == 'Aisle' or model_name == 'AisleContains':
            data = session.query(model).order_by(
                model.aisle_number).all()
        else:
            data = session.query(model).order_by(model.id).all()
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        raise

    return data


def _list_all_data_filtered(
        db, entity, entity2=None, entity3=None, entity4=None) -> list:
    data = None
    model = type(entity)
    model_name = model.__name__

    session = db.session
    session.expire_on_commit = False

    try:
        if model_name == 'Aisle' or model_name == 'AisleContains':
            data = session.query(model).filter_by(
                aisle_number=int(entity.aisle_number)).all()
        elif model_name == 'Employee':
            model2 = type(entity2)
            data = session.query(
                model, model2).filter(
                model.department_id == model2.id).order_by(
                model2.id, model.id).all()
        elif model_name == 'Product':
            model2 = type(entity2)
            model3 = type(entity3)
            model4 = type(entity4)

            data = session.query(
                model, model2, model3, model4).filter(
                model.department_id == model2.id).filter(
                model.id == model3.product_id).filter(
                model3.aisle_number == model4.aisle_number).order_by(
                model.id).all()
        else:
            data = session.query(model).filter_by(
                id=int(entity.id)).all()
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        raise

    return data


def _list_one_or_none_data(db, entity, entity2=None):
    data = None
    model = type(entity)
    model_name = model.__name__

    session = db.session
    session.expire_on_commit = False

    try:
        if model_name == 'Aisle' or model_name == 'AisleContains':
            if entity2 is None:
                data = session.query(model).filter_by(
                    aisle_number=entity.aisle_number).one_or_none()
            else:
                data = session.query(model).filter_by(
                    product_id=entity.product_id).one_or_none()
        else:
            data = session.query(model).filter_by(
                id=entity.id).one_or_none()
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        raise

    return data


def _add_entity(db, entity):
    session = db.session
    session.expire_on_commit = False

    try:
        session.add(entity)
        session.commit()
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        session.rollback()
        raise


def _update_entity(db):
    session = db.session
    session.expire_on_commit = False

    try:
        session.commit()
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        session.rollback()
        raise


def _delete_entity(db, entity=None, entity_list=None):
    session = db.session
    session.expire_on_commit = False

    try:
        if entity_list is not None:
            if len(entity_list) > 1:
                for entity in entity_list:
                    session.delete(entity)
            elif len(entity_list) == 1:
                session.delete(entity_list[0])
            else:
                raise EmptyEntityError({
                    "code": "empty_entity_object",
                    "description": "Cannot delete from empty entity object"
                })
        elif entity is not None:
            session.delete(entity)

        session.commit()
    except EmptyEntityError:
        raise
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        session.rollback()
        raise


def _get_next_id(db, entity) -> int:
    model = type(entity)
    id = 0

    session = db.session
    session.expire_on_commit = False

    try:
        if model is Aisle or model is AisleContains:
            max_id = session.query(func.max(model.aisle_name)).one_or_none()
            id = max_id[0] + 1
        else:
            max_id = session.query(func.max(model.id)).one_or_none()
            id = max_id[0] + 1
    except BaseException as e:
        tb = sys.exc_info()
        db.app.logger.info(e.with_traceback(tb[2]))
        raise

    return id
