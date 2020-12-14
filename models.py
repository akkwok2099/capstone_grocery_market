from sqlalchemy import BigInteger, Boolean, Column, Date, Float, \
    ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Aisle(Base):
    __tablename__ = 'aisles'

    aisle_number = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    products = relationship('Product', secondary='aislecontains')


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('customers_id_seq'::regclass)"))
    name = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('departments_id_seq'::regclass)"))
    name = Column(String(255))


t_lowstock = Table(
    'lowstock', metadata,
    Column('id', Integer),
    Column('name', String(255)),
    Column('department_id', BigInteger),
    Column('quantity_in_stock', Integer)
)


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('suppliers_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    phone = Column(String(255), nullable=False)


class Employee(Base):
    __tablename__ = 'employees'

    def __init__(
        self, id, name, department_id, title, emp_number,
            address, phone, wage, is_active):
        self.id = id,
        self.name = name,
        self.department_id = department_id,
        self.title = title,
        self.emp_number = emp_number,
        self.address = address,
        self.phone = phone,
        self.wage = wage,
        self.is_active = is_active

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


class Product(Base):
    __tablename__ = 'products'

    def __init__(
        self, id, name, price_per_cost_unit, cost_unit, department_id,
            quantity_in_stock, brand, production_date, best_before_date,
            plu, upc, organic, cut, animal):
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


class Providesdelivery(Base):
    __tablename__ = 'providesdelivery'

    delivery_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('providesdelivery_delivery_id_seq'::regclass)"))
    supplier_id = Column(ForeignKey('suppliers.id'), nullable=False)

    supplier = relationship('Supplier')
    products = relationship('Product', secondary='receivedfrom')


t_aislecontains = Table(
    'aislecontains', metadata,
    Column('aisle_number', ForeignKey(
        'aisles.aisle_number'), primary_key=True, nullable=False),
    Column('product_id', ForeignKey(
        'products.id'), primary_key=True, nullable=False)
)


class AisleContains(Base):
    __table__ = t_aislecontains


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


t_receivedfrom = Table(
    'receivedfrom', metadata,
    Column('product_id', ForeignKey(
        'products.id'), primary_key=True, nullable=False),
    Column('delivery_id', ForeignKey(
        'providesdelivery.delivery_id'), primary_key=True, nullable=False)
)
