from flask_wtf import FlaskForm
from wtforms import StringField, QuerySelectField, \
    DateField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Phone
from models import Department, Product, Customer


class EmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    department = QuerySelectField(
        'department', query_factory=lambda: Department.query.all()
    )
    title = StringField('title')
    emp_number = IntegerField('emp_number', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('p4511hone', validators=[DataRequired(), Phone])
    wage = IntegerField('wage')
    isactive = BooleanField(
        'isactive', validators=[DataRequired()], default=True)


class AisleForm(FlaskForm):
    aisle_number = StringField('aisle_number', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])


class CustomerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Phone])
    email = StringField('email', validators=[DataRequired(), Email])


class DepartmentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = FloatField('price_per_cost_unit', validators=[DataRequired()])
    department = QuerySelectField(
        'department', query_factory=lambda: Department.query.all()
    )
    quantity = IntegerField('quantity_in_stock', validators=[DataRequired()])
    brand = StringField('brand', validators=[DataRequired()])
    production_date = DateField('production_date', format='%d/%m/%Y')
    best_before_date = DateField('best_before_date', format='%d/%m/%Y')
    plu = IntegerField('plu', validators=[DataRequired()])
    upc = IntegerField('upc', validators=[DataRequired()])
    organic = IntegerField('organic', validators=[DataRequired()])
    cut = StringField('cut', validators=[DataRequired()])
    animal = StringField('animal', validators=[DataRequired()])


class PurchaseForm(FlaskForm):
    product = QuerySelectField(
        'product', query_factory=lambda: Product.query.all()
    )
    quantity = IntegerField('quantity', validators=[DataRequired()])
    customer = QuerySelectField(
        'customer', query_factory=lambda: Customer.query.all()
    )
    purchase_date = DateField('purchase_date', format='%d/%m/%Y')
    total = FloatField('total', validators=[DataRequired()])


class SupplierForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Phone])
