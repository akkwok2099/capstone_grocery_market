import unittest
from flask_sqlalchemy import SQLAlchemy

# Local imports...
from app import app as test_app, test_token
from config import Config


class TestApiMethods(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = test_app
        self.client = self.app.test_client

        self.app.config.from_object(Config)
        self.app.config["SQLALCHEMY_DATABASE_URI"] =\
            test_app.config['SQLALCHEMY_TEST_DATABASE_URI']
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =\
            test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""

    ###########################################################
    #
    # AISLE
    #
    # Get / Retrieve All Aisles
    #
    ###########################################################

    # Success
    def test_get_all_aisles_success(self):
        result = self.client().get(
            '/aisles',
            headers={
                'authorization': test_token,
                'test_permission': 'get:aisle'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual('Welcome Guest' in data, True)
        self.assertEqual('<h2>Manage <b>Aisles</b>' in data, True)

    # Fail - Incorrect protocal
    def test_get_all_aisles_post(self):
        result = self.client().post(
            '/aisles',
            headers={
                'authorization': test_token,
                'test_permission': 'get:aisle'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_get_all_aisles_wrong_permission(self):
        result = self.client().get(
            '/aisles',
            headers={
                'authorization': test_token,
                'test_permission': 'post:aisle'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Post / Add an Aisle
    #
    ###########################################################

    # Success
    def test_add_an_aisle_success(self):
        result = self.client().post(
            '/aisles/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:aisle'
            },
            data={
                'aisle_number': 10,
                'name': 'Silverwares'
            }
        )

        data = result.data.decode('utf8')
        # Since it's a redirect the routing method is returning,
        # it makes since for the method to return a status code
        # of 302, but the newly created 'Silverwares' is also
        # being checked in the following assert to make sure
        # it's really a success
        self.assertEqual(result.status_code, 302)
        self.assertEqual('10' in data, True)
        self.assertEqual('Silverwares' in data, True)

    # Fail - Incorrect protocal
    def test_add_an_aisle_get(self):
        result = self.client().get(
            '/aisles/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:aisle'
            },
            data={
                'aisle_number': 11,
                'name': 'Furniture'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_add_an_aisle_wrong_permission(self):
        result = self.client().post(
            '/aisles/create',
            headers={
                'authorization': test_token,
                'test_permission': 'get:aisle'
            },
            data={
                'aisle_number': 12,
                'name': 'Home Appliances'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Put / Update an Aisle
    #
    ###########################################################

    # Success
    def test_update_an_aisle_success(self):
        result = self.client().post(
            '/aisles/1',
            headers={
                'authorization': test_token,
                'test_permission': 'put:aisle'
            },
            data={
                '_method': 'PUT',
                'aisle_number': '1',
                'name': 'Tree Babies'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Fruits' in data, False)
        self.assertEqual('Tree+Babies' in data, True)

    # Fail - Incorrect protocal
    def test_update_an_aisle_get(self):
        result = self.client().get(
            '/aisles/1',
            headers={
                'authorization': test_token,
                'test_permission': 'post:aisle'
            },
            data={
                'aisle_number': '1',
                'name': 'Pets'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_update_an_aisle_wrong_permission(self):
        result = self.client().post(
            '/aisles/1',
            headers={
                'authorization': test_token,
                'test_permission': 'get:aisle'
            },
            data={
                'aisle_number': '1',
                'name': 'Home Appliances'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Delete an Aisle
    #
    ###########################################################

    # Success
    def test_delete_an_aisle_success(self):
        result = self.client().delete(
            '/aisles/10',
            headers={
                'authorization': test_token,
                'test_permission': 'delete:aisle'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Furniture' in data, False)

    # Fail - Incorrect protocal
    def test_delete_an_aisle_get(self):
        result = self.client().get(
            '/aisles/10',
            headers={
                'authorization': test_token,
                'test_permission': 'delete:aisle'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_delete_an_aisle_wrong_permission(self):
        result = self.client().delete(
            '/aisles/10',
            headers={
                'authorization': test_token,
                'test_permission': 'get:aisle'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # CUSTOMER
    #
    # Get / Retrieve All Customers
    #
    ###########################################################

    # Success
    def test_get_all_customers_success(self):
        result = self.client().get(
            '/customers',
            headers={
                'authorization': test_token,
                'test_permission': 'get:customer'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual('Welcome Guest' in data, True)
        self.assertEqual('<h2>Manage <b>Customers</b>' in data, True)

    # Fail - Incorrect protocal
    def test_get_all_customers_post(self):
        result = self.client().post(
            '/customers',
            headers={
                'authorization': test_token,
                'test_permission': 'get:customer'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_get_all_customers_wrong_permission(self):
        result = self.client().get(
            '/customers',
            headers={
                'authorization': test_token,
                'test_permission': 'post:customer'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Post / Add a Customer
    #
    ###########################################################

    # Success
    def test_add_a_customer_success(self):
        result = self.client().post(
            '/customers/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:customer'
            },
            data={
                'name': 'Alan Kwok',
                'phone': '614 123 3210',
                'email': 'alankwok1@gmail.com'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Alan+Kwok' in data, True)

    # Fail - Incorrect protocal
    def test_add_a_customer_get(self):
        result = self.client().get(
            '/customers/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:customer'
            },
            data={
                'name': 'Bruce Wayne',
                'phone': '212 123 3219',
                'email': 'bwayne@waynefoundation.com'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_add_a_customer_wrong_permission(self):
        result = self.client().post(
            '/customers/create',
            headers={
                'authorization': test_token,
                'test_permission': 'get:customer'
            },
            data={
                'name': 'Clark Kent',
                'phone': '205 123 3348',
                'email': 'ckent@thedailyplanet.com'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Put / Update a Customer
    #
    ###########################################################

    # Success
    def test_update_a_customer_success(self):
        result = self.client().post(
            '/customers/31',
            headers={
                'authorization': test_token,
                'test_permission': 'put:customer'
            },
            data={
                '_method': 'PUT',
                'name': 'Clark Kent',
                'phone': '205 123 3348',
                'email': 'ckent@thedailyplanet.com'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Alan+Kwok' in data, False)
        self.assertEqual('Clark+Kent' in data, True)

    # Fail - Incorrect protocal
    def test_update_a_customer_get(self):
        result = self.client().get(
            '/customers/31',
            headers={
                'authorization': test_token,
                'test_permission': 'post:aisle'
            },
            data={
                'name': 'Bruce Wayne',
                'phone': '212 123 3219',
                'email': 'bwayne@waynefoundation.com'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_update_a_customer_wrong_permission(self):
        result = self.client().post(
            '/customers/31',
            headers={
                'authorization': test_token,
                'test_permission': 'get:customer'
            },
            data={
                'name': 'Bruce Wayne',
                'phone': '212 123 3219',
                'email': 'bwayne@waynefoundation.com'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # DEPARTMENT
    #
    # Get / Retrieve All Departments
    #
    ###########################################################

    # Success
    def test_get_all_departments_success(self):
        result = self.client().get(
            '/departments',
            headers={
                'authorization': test_token,
                'test_permission': 'get:department'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual('Welcome Guest' in data, True)
        self.assertEqual('<h2>Manage <b>Departments</b>' in data, True)

    # Fail - Incorrect protocal
    def test_get_all_departments_post(self):
        result = self.client().post(
            '/departments',
            headers={
                'authorization': test_token,
                'test_permission': 'get:department'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_get_all_departments_wrong_permission(self):
        result = self.client().get(
            '/departments',
            headers={
                'authorization': test_token,
                'test_permission': 'post:department'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Post / Add a Department
    #
    ###########################################################

    # Success
    def test_add_a_department_success(self):
        result = self.client().post(
            '/departments/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:department'
            },
            data={
                'name': 'Electronics'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Electronics' in data, True)

    # Fail - Incorrect protocal
    def test_add_a_department_get(self):
        result = self.client().get(
            '/departments/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:department'
            },
            data={
                'name': 'Wines'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_add_a_department_wrong_permission(self):
        result = self.client().post(
            '/departments/create',
            headers={
                'authorization': test_token,
                'test_permission': 'get:department'
            },
            data={
                'name': 'Automobiles'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Put / Update a Department
    #
    ###########################################################

    # Success
    def test_update_a_department_success(self):
        result = self.client().post(
            '/departments/6',
            headers={
                'authorization': test_token,
                'test_permission': 'put:department'
            },
            data={
                '_method': 'PUT',
                'name': 'Frozens'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Electonics' in data, False)
        self.assertEqual('Frozens' in data, True)

    # Fail - Incorrect protocal
    def test_update_a_department_get(self):
        result = self.client().get(
            '/departments/6',
            headers={
                'authorization': test_token,
                'test_permission': 'post:department'
            },
            data={
                'name': 'Toys'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_update_a_department_wrong_permission(self):
        result = self.client().post(
            '/departments/6',
            headers={
                'authorization': test_token,
                'test_permission': 'get:department'
            },
            data={
                'name': 'Electronics'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # EMPLOYEE
    #
    # Get / Retrieve All Employees
    #
    ###########################################################

    # Success
    def test_get_all_employees_success(self):
        result = self.client().get(
            '/employees',
            headers={
                'authorization': test_token,
                'test_permission': 'get:employee'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual('Welcome Guest' in data, True)
        self.assertEqual('<h2>Manage <b>Employees</b>' in data, True)

    # Fail - Incorrect protocal
    def test_get_all_employees_post(self):
        result = self.client().post(
            '/employees',
            headers={
                'authorization': test_token,
                'test_permission': 'get:employee'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_get_all_employees_wrong_permission(self):
        result = self.client().get(
            '/employees',
            headers={
                'authorization': test_token,
                'test_permission': 'post:employee'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Post / Add an Employee
    #
    ###########################################################

    # Success
    def test_add_an_employee_success(self):
        result = self.client().post(
            '/employees/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:employee'
            },
            data={
                'name': 'Alan Kwok',
                'department_name': '6 - Frozens',
                'title': 'Butcher',
                'emp_number': 23451234,
                'address': '123 Main Street, Columbus, OH 43023',
                'phone': '614 234 4536',
                'wage': 12
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Alan+Kwok' in data, True)
        self.assertEqual('Butcher' in data, True)

    # Fail - Incorrect protocal
    def test_add_an_employee_get(self):
        result = self.client().get(
            '/employees/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:employee'
            },
            data={
                'name': 'Bruce Wayne',
                'department_name': '1 - Produce',
                'title': 'Waterboy',
                'emp_number': 23451239,
                'address': '123 Main Street, Gotham, NY 99999',
                'phone': '212 234 6344',
                'wage': 9
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_add_an_employee_wrong_permission(self):
        result = self.client().post(
            '/employees/create',
            headers={
                'authorization': test_token,
                'test_permission': 'get:employee'
            },
            data={
                'name': 'Bruce Wayne',
                'department_name': '1 - Produce',
                'title': 'Waterboy',
                'emp_number': 23451239,
                'address': '123 Main Street, Gotham, NY 99999',
                'phone': '212 234 6344',
                'wage': 10
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Put / Update an Employee
    #
    ###########################################################

    # Success
    def test_update_an_employee_success(self):
        result = self.client().post(
            '/employees/16',
            headers={
                'authorization': test_token,
                'test_permission': 'put:employee'
            },
            data={
                '_method': 'PUT',
                'name': 'Alan Kwok',
                'department_name': '3 - Baked Goods',
                'title': 'Baker',
                'emp_number': 23451234,
                'address': '123 Main Street, Columbus, OH 43032',
                'phone': '614 234 6344',
                'wage': 15
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Butcher' in data, False)
        self.assertEqual('Baker' in data, True)

    # Fail - Incorrect protocal
    def test_update_an_employee_get(self):
        result = self.client().get(
            '/employees/16',
            headers={
                'authorization': test_token,
                'test_permission': 'post:department'
            },
            data={
                'name': 'Bruce Wayne',
                'department_name': '3 - Baked Goods',
                'title': 'Baker',
                'emp_number': 23451234,
                'address': '123 Main Street, Gotham, NY 99999',
                'phone': '212 234 6344',
                'wage': 18
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_update_an_employee_wrong_permission(self):
        result = self.client().post(
            '/employees/6',
            headers={
                'authorization': test_token,
                'test_permission': 'get:employee'
            },
            data={
                '_method': 'PUT',
                'name': 'Bruce Wayne',
                'department_name': '3 - Baked Goods',
                'title': 'Baker',
                'emp_number': 23451234,
                'address': '123 Main Street, Gotham, NY 99999',
                'phone': '212 234 6344',
                'wage': 18
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # PRODUCT
    #
    # Get / Retrieve All Products
    #
    ###########################################################

    # Success
    def test_get_all_products_success(self):
        result = self.client().get(
            '/products',
            headers={
                'authorization': test_token,
                'test_permission': 'get:product'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual('Welcome Guest' in data, True)
        self.assertEqual('<h2>Manage <b>Products</b>' in data, True)

    # Fail - Incorrect protocal
    def test_get_all_products_post(self):
        result = self.client().post(
            '/products',
            headers={
                'authorization': test_token,
                'test_permission': 'get:product'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_get_all_products_wrong_permission(self):
        result = self.client().get(
            '/products',
            headers={
                'authorization': test_token,
                'test_permission': 'post:product'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Post / Add a Product
    #
    ###########################################################

    # Success
    def test_add_a_product_success(self):
        result = self.client().post(
            '/products/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:product'
            },
            data={
                'name': 'Noodle',
                'price_per_cost_unit': 3.5,
                'cost_unit': 'bag',
                'department_name': '4 - Pantry Items',
                'quantity_in_stock': 17,
                'brand': 'Campbell',
                'production_date': '06-07-2020',
                'best_before_date': '12-31-2021',
                'plu': 34526,
                'upc': '045637899',
                'organic': 'off',
                'cut': '',
                'animal': '',
                'aisle_name': '8 - Pantry Items'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Noodle' in data, True)
        self.assertEqual('Campbell' in data, True)

    # Fail - Incorrect protocal
    def test_add_a_product_get(self):
        result = self.client().get(
            '/products/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:product'
            },
            data={
                'name': 'iPad Pro 3',
                'price_per_cost_unit': 699.99,
                'cost_unit': 'Box',
                'department_name': '1 - Produce',
                'quantity_in_stock': 10,
                'brand': 'Apple',
                'production_date': '09-13-2018',
                'best_before_date': '',
                'plu': 24536,
                'upc': '654372898',
                'organic': 'off',
                'cut': '',
                'animal': '',
                'aisle_name': '4 - Eggs'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_add_a_product_wrong_permission(self):
        result = self.client().post(
            '/products/create',
            headers={
                'authorization': test_token,
                'test_permission': 'get:product'
            },
            data={
                'name': 'iPad Pro 3',
                'price_per_cost_unit': 699.99,
                'cost_unit': 'Box',
                'department_name': '1 - Produce',
                'quantity_in_stock': 10,
                'brand': 'Apple',
                'production_date': '09-13-2018',
                'best_before_date': '',
                'plu': 24536,
                'upc': '654372898',
                'organic': 'off',
                'cut': '',
                'animal': '',
                'aisle_name': '4 - Eggs'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Put / Update a Product
    #
    ###########################################################

    # Success
    def test_update_a_product_success(self):
        result = self.client().post(
            '/products/426',
            headers={
                'authorization': test_token,
                'test_permission': 'put:product'
            },
            data={
                '_method': 'PUT',
                'name': 'iPad Pro 3',
                'price_per_cost_unit': 699.99,
                'cost_unit': 'Box',
                'department_name': '1 - Produce',
                'quantity_in_stock': 10,
                'brand': 'Apple Inc',
                'production_date': '09-13-2018',
                'best_before_date': '',
                'plu': 24536,
                'upc': '654372898',
                'organic': 'off',
                'cut': '',
                'animal': '',
                'aisle_name': '4 - Eggs'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Noodle' in data, False)
        self.assertEqual('Campbell' in data, False)
        self.assertEqual('iPad+Pro+3' in data, True)
        self.assertEqual('Apple+Inc' in data, True)

    # Fail - Incorrect protocal
    def test_update_a_product_get(self):
        result = self.client().get(
            '/products/426',
            headers={
                'authorization': test_token,
                'test_permission': 'put:product'
            },
            data={
                '_method': 'PUT',
                'name': 'Apple Watch 3',
                'price_per_cost_unit': 359.99,
                'cost_unit': 'Box',
                'department_name': '1 - Produce',
                'quantity_in_stock': 25,
                'brand': 'Apple Inc',
                'production_date': '12-01-2020',
                'best_before_date': '',
                'plu': 24596,
                'upc': '654372854',
                'organic': 'off',
                'cut': '',
                'animal': '',
                'aisle_name': '4 - Eggs'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_update_a_product_wrong_permission(self):
        result = self.client().post(
            '/products/426',
            headers={
                'authorization': test_token,
                'test_permission': 'get:product'
            },
            data={
                '_method': 'PUT',
                'name': 'Apple Watch 3',
                'price_per_cost_unit': 359.99,
                'cost_unit': 'Box',
                'department_name': '1 - Produce',
                'quantity_in_stock': 25,
                'brand': 'Apple Inc',
                'production_date': '12-01-2020',
                'best_before_date': '',
                'plu': 24596,
                'upc': '654372854',
                'organic': 'off',
                'cut': '',
                'animal': '',
                'aisle_name': '4 - Eggs'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # SUPPLIER
    #
    # Get / Retrieve All Suppliers
    #
    ###########################################################

    # Success
    def test_get_all_suppliers_success(self):
        result = self.client().get(
            '/suppliers',
            headers={
                'authorization': test_token,
                'test_permission': 'get:supplier'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual('Welcome Guest' in data, True)
        self.assertEqual('<h2>Manage <b>Suppliers</b>' in data, True)

    # Fail - Incorrect protocal
    def test_get_all_suppliers_post(self):
        result = self.client().post(
            '/products',
            headers={
                'authorization': test_token,
                'test_permission': 'get:supplier'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_get_all_suppliers_wrong_permission(self):
        result = self.client().get(
            '/suppliers',
            headers={
                'authorization': test_token,
                'test_permission': 'post:supplier'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Post / Add a Supplier
    #
    ###########################################################

    # Success
    def test_add_a_supplier_success(self):
        result = self.client().post(
            '/suppliers/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:supplier'
            },
            data={
                'name': 'Fatboy Wholesale Ltd',
                'address': '12345 Fat Street, Chicago, IL 45327',
                'phone': '342 267 1234'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Fatboy+Wholesale+Ltd' in data, True)

    # Fail - Incorrect protocal
    def test_add_a_supplier_get(self):
        result = self.client().get(
            '/suppliers/create',
            headers={
                'authorization': test_token,
                'test_permission': 'post:supplier'
            },
            data={
                'name': 'Amazon.com',
                'address': '410 Terry Ave North, Seattle, WA 98109',
                'phone': '206 266 1000'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_add_a_supplier_wrong_permission(self):
        result = self.client().post(
            '/suppliers/create',
            headers={
                'authorization': test_token,
                'test_permission': 'get:supplier'
            },
            data={
                'name': 'Amazon.com',
                'address': '410 Terry Ave North, Seattle, WA 98109',
                'phone': '206 266 1000'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)

    ###########################################################
    #
    # Put / Update a Product
    #
    ###########################################################

    # Success
    def test_update_a_supplier_success(self):
        result = self.client().post(
            '/suppliers/21',
            headers={
                'authorization': test_token,
                'test_permission': 'put:supplier'
            },
            data={
                '_method': 'PUT',
                'name': 'Amazon.com',
                'address': '410 Terry Ave North, Seattle, WA 98109',
                'phone': '206 266 1000'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 302)
        self.assertEqual('Fatboy+Wholesale+Ltd' in data, False)
        self.assertEqual('Chicago' in data, False)
        self.assertEqual('Amazon' in data, True)
        self.assertEqual('Seattle' in data, True)

    # Fail - Incorrect protocal
    def test_update_a_supplier_get(self):
        result = self.client().get(
            '/suppliers/21',
            headers={
                'authorization': test_token,
                'test_permission': 'put:supplier'
            },
            data={
                '_method': 'PUT',
                'name': 'SpartanNash',
                'address': '850 76th St SW, Byron Center, MI 49315',
                'phone': '616 878 2000'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 405)
        self.assertEqual('Incorrect transfer protocol' in data, True)

    # Fail - Wrong Permission
    def test_update_a_supplier_wrong_permission(self):
        result = self.client().post(
            '/suppliers/21',
            headers={
                'authorization': test_token,
                'test_permission': 'get:supplier'
            },
            data={
                '_method': 'PUT',
                'name': 'SpartanNash',
                'address': '850 76th St SW, Byron Center, MI 49315',
                'phone': '616 878 2000'
            }
        )

        data = result.data.decode('utf8')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            'Authentication and/or authorization error' in data, True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
