from models import Employee, Product


class EmployeeDto(Employee):
    def __init__(
        self, department_name, id, name, department_id, title,
            emp_number, address, phone, wage, is_active):
        super().__init__(
            id, name, department_id, title,
            emp_number, address, phone, wage, is_active)
        self.department_name = department_name


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
