-- drop existing database and recreate it
--DROP DATABASE IF EXISTS grocery_market;
--CREATE DATABASE grocery_market;

-- drop schema which contains all tables and views and recreate the schema
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- restore default grants
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- create tables and views
CREATE TABLE Customers(
    id SERIAL,
    name VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE Departments(
    id SERIAL,
    name VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE Suppliers(
    id Serial,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Employees(
    id Serial,
    name VARCHAR(255) NOT NULL,
    department_id BIGINT,
    title VARCHAR(255),
    emp_number BIGINT NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(255),
    wage INT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY(id),
    FOREIGN KEY(department_id) REFERENCES Departments(id)
);

CREATE TABLE Products(
    id Serial,
    name VARCHAR(255) NOT NULL,
    price_per_cost_unit FLOAT NOT NULL,
    cost_unit VARCHAR(255) NOT NULL,
    department_id BIGINT NOT NULL,
    quantity_in_stock INT,
    brand VARCHAR(255),
    production_date VARCHAR(10),
    best_before_date VARCHAR(10),
    plu INT,
    upc VARCHAR(20),
    organic INT,
    cut VARCHAR(255),
    animal VARCHAR(255),
    PRIMARY KEY(id),
    FOREIGN KEY(department_id) REFERENCES Departments(id)
);

CREATE VIEW LowStock AS
SELECT id, name, department_id, quantity_in_stock
FROM Products
WHERE quantity_in_stock < 7;

CREATE TABLE Aisles(
    aisle_number INT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(aisle_number)
);

CREATE TABLE AisleContains(
    aisle_number INT,
    product_id INT,
    PRIMARY KEY(aisle_number, product_id),
    FOREIGN KEY(product_id) REFERENCES Products(id),
    FOREIGN KEY(aisle_number) REFERENCES Aisles(aisle_number)
);

CREATE TABLE ProvidedBy(
    product_id INT,
    supplier_id INT,
    PRIMARY KEY(supplier_id, product_id),
    FOREIGN KEY(supplier_id) REFERENCES Suppliers(id),
    FOREIGN KEY(product_id) REFERENCES Products(id)
);

CREATE TABLE ProvidesDelivery(
    delivery_id Serial,
    supplier_id INT NOT NULL,
    PRIMARY KEY(delivery_id),
    FOREIGN KEY(supplier_id) REFERENCES Suppliers(id)
);

CREATE TABLE ReceivedFrom(
    product_id INT,
    delivery_id INT,
    PRIMARY KEY(product_id, delivery_id),
    FOREIGN KEY(product_id) REFERENCES Products(id),
    FOREIGN KEY(delivery_id) REFERENCES ProvidesDelivery(delivery_id)
);

CREATE TABLE Purchases(
    id Serial,
    product_id INT,
    quantity INT,
    customer_id INT,
    purchase_date VARCHAR(10),
    total FLOAT,
    is_cancelled BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(id, product_id),
    FOREIGN KEY(product_id) REFERENCES Products(id),
    FOREIGN KEY(customer_id) REFERENCES Customers(id)
);

-- reset ID sequences
ALTER SEQUENCE customers_id_seq restart with 1;
ALTER SEQUENCE suppliers_id_seq restart with 1;
ALTER SEQUENCE employees_id_seq restart with 1;
ALTER SEQUENCE products_id_seq restart with 1;
ALTER SEQUENCE providesdelivery_delivery_id_seq restart with 1;
ALTER SEQUENCE purchases_id_seq restart with 1;


-- insertion into Customers
INSERT INTO Customers VALUES(1, 'Harry Potter', '000 731 1980', 'theboywholived@gmail.com');
INSERT INTO Customers VALUES(2, 'Lily Potter', '000 731 1980', 'lpotter@gmail.com');
INSERT INTO Customers VALUES(3, 'James Potter', '000 731 1980', 'jpotter@gmail.com');
INSERT INTO Customers VALUES(4, 'Hermione Granger', '555 123 1979', 'hgranger@icloud.com');
INSERT INTO Customers VALUES(5, 'Ron Weasley', '604 301 1979', 'roonilwazlib@hotmail.com');
INSERT INTO Customers VALUES(6, 'Ginny Weasley', '778 872 1928', 'ginnyw@gmail.com');
INSERT INTO Customers VALUES(7, 'Fred Weasley', '604 976 3693', 'fweasley@gmail.com');
INSERT INTO Customers VALUES(8, 'George Weasley', '604 976 3693', 'gweasley@gmail.com');
INSERT INTO Customers VALUES(9, 'Arthur Weasley', '604 976 3693', 'aweasley@gmail.com');
INSERT INTO Customers VALUES(10, 'Molly Weasley', '604 976 3693', 'mweasley@gmail.com');
INSERT INTO Customers VALUES(11, 'Percy Weasley', '604 976 3693', 'pweasley@gmail.com');
INSERT INTO Customers VALUES(12, 'Bill Weasley', '604 976 3693', 'bweasley@gmail.com');
INSERT INTO Customers VALUES(13, 'Charlie Weasley', '604 976 3693', 'cweasley@gmail.com');
INSERT INTO Customers VALUES(14, 'Lord Voldemort', '778 192 3928', 'tmriddle@hotmail.com');
INSERT INTO Customers VALUES(15, 'Draco Malfoy', '908 392 1928', 'mini_mr_malfoy@gmail.com');
INSERT INTO Customers VALUES(16, 'Lucius Malfoy', '908 392 1928', 'lmalfoy@gmail.com');
INSERT INTO Customers VALUES(17, 'Narcissa Malfoy', '908 392 1928', 'nmalfoy@gmail.com');
INSERT INTO Customers VALUES(18, 'Neville Longbottom', '498 192 3091', 'longbottom@live.com');
INSERT INTO Customers VALUES(19, 'Dudley Dursley', '930 409 9380', 'ddursley@hotmail.com');
INSERT INTO Customers VALUES(20, 'Vernon Dursley', '930 409 9380', 'vdursley@hotmail.com');
INSERT INTO Customers VALUES(21, 'Petunia Dursley', '930 409 9380', 'pdursley@hotmail.com');
INSERT INTO Customers VALUES(22, 'Severus Snape', '928 182 0493', 'snivellus@gmail.com');
INSERT INTO Customers VALUES(23, 'Rubeus Hagrid', '458 392 1029', 'rhagrid@hotmail.com');
INSERT INTO Customers VALUES(24, 'Minverva McGonagall', '893 928 0933', 'mmcgonagall@gmail.com');
INSERT INTO Customers VALUES(25, 'Albus Dumbledore', '920 849 9145', 'adumbledore@gmail.com');
INSERT INTO Customers VALUES(26, 'Hedwig', '839 920 1234', 'im_actually_an_owl@hotmail.com');
INSERT INTO Customers VALUES(27, 'Crookshanks', '555 983 0298', 'cat@icloud.com');
INSERT INTO Customers VALUES(28, 'Sirius Black', '649 563 4723', 'sblack@gmail.com');
INSERT INTO Customers VALUES(29, 'Lavender Brown', '604 983 6941', 'lbrown@hotmail.com');
INSERT INTO Customers VALUES(30, 'Colin Creevey', '778 961 6435', 'ccreevey@gmail.com');

-- insertion into Suppliers
INSERT INTO Suppliers VALUES(1, 'Saputo Dairy Products Canada', '6800 Lougheed Highway, Burnaby, BC V5A 1W2', '1 800 672 8866');
INSERT INTO Suppliers VALUES(2, 'Gordon Food Services', '1700 Cliveden Avenue, Delta, BC V3M 6T2', '800 663 1695');
INSERT INTO Suppliers VALUES(3, 'Yen Bros. Food Service', '1988 Vernon Drive, Vancouver, BC V6A 3Y6', '604 255 6522');
INSERT INTO Suppliers VALUES(4, 'Arctic Meat & Sausage', '1606 Kebet Way, Port Coquitlam, BC V3C 5W9', '604 472 9995');
INSERT INTO Suppliers VALUES(5, 'Lekker Food Distribution Ltd.', '2670 Wilfert Road, Victoria, BC V9B 5Z3', '877 788 0377');
INSERT INTO Suppliers VALUES(6, 'Get Sauced & Spiced Inc.', '58 Avenue, Surrey, BC V8H 4S9', '780 462 2418');
INSERT INTO Suppliers VALUES(7, 'Orkin Canada', '123 Missisauga Street, Vancouver, BC V7A 0E3', '800 800 6754');
INSERT INTO Suppliers VALUES(8, 'Grainworks Inc.', '921 Vulcan Avenue, Richmond, BC V8A 3H1', '800 563 3756');
INSERT INTO Suppliers VALUES(9, 'Harvest Corporation', '249 Missisauga Street, Vancouver, BC V9U 1H3', '888 925 6644');
INSERT INTO Suppliers VALUES(10, 'The Leaky Cauldron', '938 Diagon Alley, London, UK, EC', '800 172 4532');
INSERT INTO Suppliers VALUES(11, 'Bondi Produce', '188 New Toronto St, Etobicoke, ON M8V 2E8', '416 252-7799');
INSERT INTO Suppliers VALUES(12, 'Augusta Fruit Market Ltd', '65 Nassau St, Toronto, ON M5T 1M3', '416 593-9754');
INSERT INTO Suppliers VALUES(13, 'Castle Fruit Retail & Wholesale Produce', '80 Kensington Ave, Toronto, ON M5T 2K1', '416 593-9262');
INSERT INTO Suppliers VALUES(14, 'Venerica Meat', '3348 Dundas St W, Toronto, ON M6P 2A4', '416 623-7878');
INSERT INTO Suppliers VALUES(15, 'Avalon Dairy', '7985 N Fraser Way, Burnaby, BC V5J 4Z5', '604 456-0550');
INSERT INTO Suppliers VALUES(16, 'Smokey Bay Seafood Company Ltd', '896 Cambie St, Vancouver, BC V6B 2P4', '604 568-4310');
INSERT INTO Suppliers VALUES(17, 'Oceanfood Sales', '1909 E Hastings St, Vancouver, BC V5L 1T5', '604 255-1414');
INSERT INTO Suppliers VALUES(18, 'Deluxe Seafood Vancouver Ltd', '#106-366 East Kent Ave, South Vancouver, BC V5X 4N6', '604 662-7999');
INSERT INTO Suppliers VALUES(19, 'Winning Seafood Co', '1568 Venables St, Vancouver, BC V5L 2G9', '604 251-3121');
INSERT INTO Suppliers VALUES(20, 'Blundell Seafoods Ltd', '11351 River Rd, Richmond, BC V6X 1Z6', '604 270-3300');

-- insertion into Departments
INSERT INTO Departments VALUES(1, 'Produce');
INSERT INTO Departments VALUES(2, 'Meat and Seafood');
INSERT INTO Departments VALUES(3, 'Baked Goods');
INSERT INTO Departments VALUES(4, 'Pantry Items');
INSERT INTO Departments VALUES(5, 'Eggs and Dairy');

-- insertion into Employees
INSERT INTO Employees VALUES(1, 'Ben Ling', 5, 'Stocker', 948398198, '2366 Main Mall, Vancouver, BC VH3 0A2', '604 822 3061', 0, TRUE);
INSERT INTO Employees VALUES(2, 'Daenerys Targaryen', 5, 'Manager', 7685437775, '123 House Targaryen, Dragonstone, BC VK8 2H9', '777 777 7777', 0, TRUE);
INSERT INTO Employees VALUES(3, 'Jon Snow', 2, 'Manager', 901982091, '224 Winter Is Coming, North, BC, VA7 4K8', '783 309 1923', 0, TRUE);
INSERT INTO Employees VALUES(4, 'Samwell Tarly', 2, 'Stocker', 971361789, '3366 Main Mall, Vancouver, BC V1M 3A0', '604 699 6993', 10, TRUE);
INSERT INTO Employees VALUES(5, 'Eddard Stark', 1, 'Stocker', 993156678, '9899 East Mall, Vancouver, BC V0A 9L6', '778 896 3644', 10, TRUE);
INSERT INTO Employees VALUES(6, 'Sansa Stark', 4, 'Manager', 935986412, '9899 East Mall, Vancouver, BC V0A 9L6', '778 896 3644', 20, TRUE);
INSERT INTO Employees VALUES(7, 'Arya Stark', 5, 'Manager', 964799315, '9899 East Mall, Vancouver, BC V0A 9L6', '778 896 3644', 20, TRUE);
INSERT INTO Employees VALUES(8, 'Bran Stark', 1, 'Stocker', 911364899, '9899 East Mall, Vancouver, BC V0A 9L6', '778 896 3644', 10, TRUE);
INSERT INTO Employees VALUES(9, 'Robb Stark', 4, 'Stocker', 944651997, '9899 East Mall, Vancouver, BC V0A 9L6', '778 896 3644', 10, TRUE);
INSERT INTO Employees VALUES(10, 'Margaery Tyrell', 3, 'Manager', 961694366, '226 Main Street, Highgarden, BC, V7L 3H7', '778 962 2264', 20, TRUE);
INSERT INTO Employees VALUES(11, 'Khal Drogo', 5, 'Stocker', 943116456, '6324 West Mall, Vancouver, BC, V7A 5M5', '604 443 6187', 10, TRUE);
INSERT INTO Employees VALUES(12, 'Yuchen Lin', 4, 'Stocker', 986456189, '999 Brilliant Boy Ave, Vancouver, BC, V8P 9L1', '976 359 1659', 10, TRUE);
INSERT INTO Employees VALUES(13, 'Hannah Lin', 1, 'Manager', 933641391, '1616 East Mall, Vancouver, BC, V0L 3M1', '604 919 3136', 25, TRUE);
INSERT INTO Employees VALUES(14, 'Jordan De Mello', 2, 'Manager', 976131971, '2525 West Mall, Vancouver, BC, V0L 3A3', '778 689 1369', 25, TRUE);
INSERT INTO Employees VALUES(15, 'Ed Knorr', 1, 'Stocker', 931236761, '988 Database Drive, Vancouver, BC, V0L 9A3', '604 977 2163', 15, TRUE);

-- insertion into Products

-- fruits insertion
INSERT INTO Products VALUES(1, 'Apples (Ambrosia)', 1.59, 'lb', 1, 256, null, '12-01-2017', '12-15-2017', 3438, null, 0, null, null);
INSERT INTO Products VALUES(2, 'Apples (Fuji)', 1.49, 'lb', 1, 31, null, '12-09-2017', '12-23-2017', 4129, null, 0, null, null);
INSERT INTO Products VALUES(3, 'Apples (Gala)', 1.19, 'lb', 1, 30, null, '12-07-2017', '12-21-2017', 4133, null, 0, null, null);
INSERT INTO Products VALUES(4, 'Apples (Gala)', 1.29, 'lb', 1, 5, null, '12-05-2017', '12-19-2017', 94133, null, 1, null, null);
INSERT INTO Products VALUES(5, 'Apples (Granny Smith)', 1.39, 'lb', 1, 15, null, '12-05-2017', '12-19-2017', 4017, null, 0, null, null);
INSERT INTO Products VALUES(6, 'Bananas', 0.79, 'lb', 1, 50, null, '12-19-2017', '12-23-2017', 4011, null, 0, null, null);
INSERT INTO Products VALUES(7, 'Bananas', 0.99, 'lb', 1, 50, null, '12-19-2017', '12-23-2017', 94011, null, 1, null, null);
INSERT INTO Products VALUES(8, 'Oranges (Navel)', 1.19, 'lb', 1, 3, null, '12-10-2017', '12-24-2017', 4012, null, 1, null, null);
INSERT INTO Products VALUES(9, 'Oranges (Valencia)', 1.29, 'lb', 1, 21, null, '12-06-2017', '12-25-2017', 4013, null, 1, null, null);
INSERT INTO Products VALUES(10, 'Strawberries', 4.99, 'lb', 1, 20, null, '12-10-2017', '12-13-2017', 3355, null, 0, null, null);
INSERT INTO Products VALUES(11, 'Blueberries', 3.99, 'lb', 1, 60, null, '12-10-2017', '12-13-2017', 4240, null, 0, null, null);
INSERT INTO Products VALUES(12, 'Raspberries', 3.49, 'lb', 1, 2, null, '12-10-2017', '12-13-2017', 4244, null, 0, null, null);

-- vegetables insertion
INSERT INTO Products VALUES(13, 'Lettuce (Iceberg)', 0.99, 'ct', 1, 20, null, '12-01-2017', '12-08-2017', 4061, null, 0, null, null);
INSERT INTO Products VALUES(14, 'Lettuce (Romaine)', 1.29, 'ct', 1, 23, null, '12-02-2017', '12-09-2017', 3097, null, 0, null, null);
INSERT INTO Products VALUES(15, 'Spinach', 1.59, 'bunch', 1, 21, null, '12-10-2017', '12-13-2017', 4090, null, 0, null, null);
INSERT INTO Products VALUES(16, 'Watercress', 1.99, 'bunch', 1, 2, null, '12-10-2017', '12-13-2017', 4815, null, 0, null, null);
INSERT INTO Products VALUES(17, 'Bok Choy (Baby)', 1.29, 'bunch', 1, 14, null, '12-10-2017', '12-13-2017', 4545, null, 0, null, null);
INSERT INTO Products VALUES(18, 'Bok Choy (Shanghai)', 0.99, 'bunch', 1, 15, null, '12-10-2017', '12-13-2017', 3163, null, 0, null, null);
INSERT INTO Products VALUES(19, 'Potatoes (Russet)', 0.99, 'lb', 1, 2, null, '12-01-2017', '12-30-2017', 4072, null, 0, null, null);
INSERT INTO Products VALUES(20, 'Potatoes (Red)', 1.29, 'lb', 1, 22, null, '12-02-2017', '12-31-2017', 4073, null, 0, null, null);
INSERT INTO Products VALUES(21, 'Potatoes (Sweet)', 1.49, 'lb', 1, 10, null, '12-01-2017', '12-30-2017', 4726, null, 0, null, null);
INSERT INTO Products VALUES(22, 'Squash (Acorn)', 0.99, 'lb', 1, 14, null, '11-01-2017', '12-31-2017', 3143, null, 0, null, null);
INSERT INTO Products VALUES(23, 'Squash (Kabocha)', 0.99, 'lb', 1, 10, null, '11-01-2017', '12-31-2017', 4769, null, 0, null, null);
INSERT INTO Products VALUES(24, 'Squash (Butternut)', 0.99, 'lb', 1, 4, null, '11-01-2017', '12-31-2017', 4759, null, 0, null, null);
INSERT INTO Products VALUES(25, 'Carrots (Loose)', 1.29, 'lb', 1, 20, null, '12-01-2017', '12-30-2017', 4562, null, 0, null, null);
INSERT INTO Products VALUES(26, 'Carrots (Loose)', 1.49, 'lb', 1, 34, null, '12-01-2017', '12-30-2017', 94562, null, 0, null, null);
INSERT INTO Products VALUES(27, 'Onions (Red)', 1.29, 'lb', 1, 20, null, '11-01-2017', '12-31-2017', 4082, null, 0, null, null);
INSERT INTO Products VALUES(28, 'Onions (Yellow)', 1.29, 'lb', 1, 5, null, '11-01-2017', '12-31-2017', 4093, null, 0, null, null);
INSERT INTO Products VALUES(29, 'Onions (White)', 1.19, 'lb', 1, 4, null, '11-01-2017', '12-31-2017', 4663, null, 0, null, null);
INSERT INTO Products VALUES(30, 'Onions (Pearl)', 2.49, 'lb', 1, 27, null, '11-01-2017', '12-31-2017', 4660, null, 0, null, null);
INSERT INTO Products VALUES(31, 'Garlic', 3.99, 'lb', 1, 20, null, '11-01-2017', '12-31-2017', 3399, null, 0, null, null);
INSERT INTO Products VALUES(32, 'Ginger', 2.49, 'lb', 1, 12, null, '11-01-2017', '12-31-2017', 4612, null, 0, null, null);

-- dairy insertion
INSERT INTO Products VALUES(100, 'Milk (Skim)', 2.29, 'L', 5, 7, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125003', 0, null, null);
INSERT INTO Products VALUES(101, 'Milk (1%)', 2.29, 'L', 5, 8, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125004', 0, null, null);
INSERT INTO Products VALUES(102, 'Milk (2%)', 2.29, 'L', 5, 3, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125005', 0, null, null);
INSERT INTO Products VALUES(103, 'Milk (Whole)', 2.29, 'L', 5, 4, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125006', 0, null, null);
INSERT INTO Products VALUES(104, 'Half and Half (10%)', 2.99, 'L', 5, 10, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125007', 0, null, null);
INSERT INTO Products VALUES(105, 'Milk (Skim)', 2.29, 'L', 5, 10, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125008', 1, null, null);
INSERT INTO Products VALUES(106, 'Milk (1%)', 2.29, 'L', 5, 1, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125009', 1, null, null);
INSERT INTO Products VALUES(107, 'Milk (2%)', 2.29, 'L', 5, 11, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125010', 1, null, null);
INSERT INTO Products VALUES(108, 'Milk (Whole)', 2.29, 'L', 5, 12, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125011', 1, null, null);
INSERT INTO Products VALUES(109, 'Milk (2% Chocolate)', 2.99, 'L', 5, 100, 'Dairyland', '12-01-2017', '12-14-2017', null, '068700125011', 1, null, null);
INSERT INTO Products VALUES(110, 'Milk (Soy)', 2.29, 'L', 5, 5, 'Silk', '12-01-2017', '12-20-2017', null, '068700125012', 1, null, null);
INSERT INTO Products VALUES(111, 'Milk (Unsweetened Soy)', 2.29, 'L', 5, 4, 'Silk', '12-01-2017', '12-20-2017', null, '068700125013', 1, null, null);
INSERT INTO Products VALUES(112, 'Yogurt (Vanilla, 6-pack)', 3.97, 'ct', 5, 1, 'Silk', '12-01-2017', '12-20-2017', null, '068700125012', 0, null, null);
INSERT INTO Products VALUES(113, 'Yogurt (Vanilla, 6-pack)', 4.97, 'ct', 5, 3, 'Silk', '12-01-2017', '12-20-2017', null, '068700125012', 1, null, null);
INSERT INTO Products VALUES(114, 'Yogurt (Strawberry, 6-pack)', 3.97, 'ct', 5, 10, 'Silk', '12-01-2017', '12-20-2017', null, '068700125013', 0, null, null);
INSERT INTO Products VALUES(115, 'Yogurt (Fat-free, 6-pack)', 3.97, 'ct', 5, 10, 'Silk', '12-01-2017', '12-20-2017', null, '068700125012', 0, null, null);
INSERT INTO Products VALUES(116, 'Butter (Salted)', 3.29, 'L', 5, 10, 'Silk', '12-01-2017', '12-20-2017', null, '068700125013', 0, null, null);
INSERT INTO Products VALUES(117, 'Butter (Unsalted)', 3.29, 'L', 5, 16, 'Silk', '12-01-2017', '12-20-2017', null, '068700125012', 0, null, null);
INSERT INTO Products VALUES(118, 'Cheese (Mozzarella)', 2.29, 'L', 5, 17, 'Silk', '12-01-2017', '12-20-2017', null, '068700125013', 0, null, null);
INSERT INTO Products VALUES(119, 'Cheese (Cheddar)', 2.29, 'L', 5, 12, 'Silk', '12-01-2017', '12-20-2017', null, '068700125013', 0, null, null);
INSERT INTO Products VALUES(120, 'Cheese (Parmesan)', 2.29, 'L', 5, 10, 'Silk', '12-01-2017', '12-20-2017', null, '068700125013', 0, null, null);

-- eggs insertion
INSERT INTO Products VALUES(150, 'Eggs (12 count)', 3.99, 'pack', 5, 11, 'Kirkland Signature', '12-01-2017', '12-20-2017', null, '062639410124', 0, null, null);
INSERT INTO Products VALUES(151, 'Eggs (Brown, 12 count)', 4.99, 'pack', 5, 10, 'Golden Valley', '12-01-2017', '12-20-2017', null, '062639410125', 0, null, null);
INSERT INTO Products VALUES(152, 'Eggs (Omega-3, 12 count)', 5.99, 'pack', 5, 32, 'Born 3 Omega-3', '12-01-2017', '12-20-2017', null, '666933900420', 0, null, null);

-- meat and seafood insertion
INSERT INTO Products VALUES(200, 'Chicken Breast', 5.99, 'lb', 2, 11, 'Kirkland Signature', '12-01-2017', '12-03-2017', null, '233841823921', 0, null, 'Chicken');
INSERT INTO Products VALUES(201, 'Chicken Breast', 6.99, 'lb', 2, 2, 'Green Way', '12-05-2017', '12-07-2017', null, '233841823920', 1, null, 'Chicken');
INSERT INTO Products VALUES(202, 'Chicken Thighs', 4.99, 'lb', 2, 13, 'Kirkland Signature', '12-01-2017', '12-03-2017', null, '233841823919', 0, null, 'Chicken');
INSERT INTO Products VALUES(203, 'Stew Meat', 7.99, 'lb', 2, 15, 'Kirkland Signature', '12-05-2017', '12-08-2017', null, '233841823910', 0, 'Chuck', 'Beef');
INSERT INTO Products VALUES(204, 'Ground Beef', 4.99, 'lb', 2, 16, 'Kirkland Signature', '12-01-2017', '12-03-2017', null, '233841823821', 0, null, 'Beef');
INSERT INTO Products VALUES(205, 'Steak', 6.99, 'lb', 2, 10, 'Western Canadian', '12-05-2017', '12-07-2017', null, '233841823822', 0, 'Sirloin', 'Beef');
INSERT INTO Products VALUES(206, 'Steak', 7.99, 'lb', 2, 17, 'Western Canadian', '12-01-2017', '12-03-2017', null, '233841823823', 0, 'Flank', 'Beef');
INSERT INTO Products VALUES(207, 'Steak', 7.99, 'lb', 2, 10, 'Western Canadian', '12-05-2017', '12-08-2017', null, '233841823824', 0, 'Tenderloin', 'Beef');
INSERT INTO Products VALUES(208, 'Cod Fillets', 6.99, 'lb', 2, 30, null, '12-05-2017', '12-08-2017', null, '233841823825', 0, 'Fillet', 'Cod');
INSERT INTO Products VALUES(209, 'Sole Fillets', 6.99, 'lb', 2, 12, null, '12-05-2017', '12-08-2017', null, '233841823826', 0, 'Fillet', 'Sole');
INSERT INTO Products VALUES(210, 'Tilapia (Fresh)', 6.99, 'lb', 2, 4, null, '12-05-2017', '12-08-2017', null, '233841823827', 0, null, 'Tilapia');
INSERT INTO Products VALUES(211, 'Salmon (Fresh)', 7.99, 'lb', 2, 10, null, '12-05-2017', '12-08-2017', null, '233841823828', 0, 'Fillet', 'Salmon');
INSERT INTO Products VALUES(212, 'Salmon (Fresh)', 8.99, 'lb', 2, 10, null, '12-05-2017', '12-08-2017', null, '233841823829', 1, 'Fillet', 'Salmon');

-- baked goods insertion
INSERT INTO Products VALUES(300, 'Bread (White)', 2.99, 'ct', 3, 4, 'Villagio', '12-01-2017', '12-06-2017', null, '006872100350', 0, null, null);
INSERT INTO Products VALUES(301, 'Bread (Whole Wheat)', 3.99, 'ct', 3, 7, 'Pepperidge Farms', '12-01-2017', '12-06-2017', null, '014100071013', 0, null, null);
INSERT INTO Products VALUES(302, 'Everything Bagel (6 count)', 4.99, 'pack', 3, 15, 'Sara Lee', '12-01-2017', '12-06-2017', null, '072945610033', 0, null, null);
INSERT INTO Products VALUES(303, 'Mini Cinnamon Raisin Bagel (6 count)', 4.99, 'pack', 3, 25, 'Pepperidge Farms', '12-01-2017', '12-06-2017', null, '014100092599', 0, null, null);
INSERT INTO Products VALUES(304, 'Bread (Rye)', 3.99, 'ct', 3, 9, 'Silver Hills Bakery', '12-01-2017', '12-06-2017', null, '014100071013', 1, null, null);
INSERT INTO Products VALUES(305, 'Bread (Spelt)', 4.99, 'ct', 3, 20, 'Silver Hills Bakery', '12-01-2017', '12-06-2017', null, '072945610033', 1, null, null);
INSERT INTO Products VALUES(306, 'Sprouted Bagel (6 count)', 4.99, 'pack', 3, 22, 'Silver Hills Bakery', '12-01-2017', '12-06-2017', null, '014100092599', 1, null, null);
INSERT INTO Products VALUES(307, 'Doughnut', 0.99, 'ct', 3, 3, 'Bake Shop', '12-01-2017', '12-03-2017', null, null, 0, null, null);

-- pantry items insertion
INSERT INTO Products VALUES(400, 'All-Purpose Flour (Original)', 1.19, 'lb', 4, 32, 'Robin Hood', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(401, 'All-Purpose Flour (Whole Wheat)', 1.29, 'lb', 4, 30, 'Robin Hood', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(402, 'White Sugar', 0.89, 'lb', 4, 3, 'Rogers', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(403, 'Brown Sugar', 0.99, 'lb', 4, 20, 'Rogers', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(404, 'Iodized Table Salt', 0.49, 'lb', 4, 34, 'Windsor', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(405, 'Black Pepper', 0.59, 'lb', 4, 31, 'Windsor', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(406, 'Ground Cinnamon', 3.99, 'lb', 4, 10, 'Club House', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(407, 'Chili Flakes', 4.59, 'lb', 4, 20, 'Club House', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(408, 'White Rice', 1.59, 'lb', 4, 12, 'Rooster', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(409, 'Scoobi Do Pasta', 0.69, 'lb', 4, 20, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(410, 'Fusili', 0.69, 'lb', 4, 21, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(411, 'Penne Rigate', 0.69, 'lb', 4, 31, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(412, 'Elbow Pasta', 0.69, 'lb', 4, 4, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(413, 'Spaghetti', 0.69, 'lb', 4, 5, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(414, 'Linguini', 0.69, 'lb', 4, 6, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(415, 'Spaghettini', 0.69, 'lb', 4, 10, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(416, 'Farfalle', 0.69, 'lb', 4, 20, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(417, 'Ditali', 0.69, 'lb', 4, 33, 'Italpasta', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(418, 'Fusili', 0.69, 'lb', 4, 26, 'Barilla', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(419, 'Penne Rigate', 0.69, 'lb', 4, 20, 'Barilla', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(420, 'Elbow Pasta', 0.69, 'lb', 4, 40, 'Barilla', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(421, 'Spaghetti', 0.69, 'lb', 4, 10, 'Barilla', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(422, 'Linguini', 0.69, 'lb', 4, 32, 'Barilla', '10-01-2017', '12-31-2017', null, null, 0, null, null);
INSERT INTO Products VALUES(423, 'Sriracha Chili Sauce', 2.99, 'ct', 4, 300, 'Huy Fong', '11-01-2017', '12-31-2017', null, '024463061095', 0, null, null);
INSERT INTO Products VALUES(424, 'Tomato Ketchup', 3.99, 'ct', 4, 100, 'Heinz', '11-01-2017', '12-31-2017', null, '013000001243', 0, null, null);
INSERT INTO Products VALUES(425, 'Soy Sauce', 3.99, 'ct', 4, 4, 'Kikkoman', '11-01-2017', '12-31-2017', null, '041390000829', 0, null, null);

-- insertion into Aisles
INSERT INTO Aisles VALUES(1, 'Fruits');
INSERT INTO Aisles VALUES(2, 'Vegetables');
INSERT INTO Aisles VALUES(3, 'Dairy');
INSERT INTO Aisles VALUES(4, 'Eggs');
INSERT INTO Aisles VALUES(5, 'Meats');
INSERT INTO Aisles VALUES(6, 'Seafood');
INSERT INTO Aisles VALUES(7, 'Baked Goods');
INSERT INTO Aisles VALUES(8, 'Pantry Items');

-- insertion into AisleContains
INSERT INTO AisleContains VALUES(1, 1);
INSERT INTO AisleContains VALUES(1, 2);
INSERT INTO AisleContains VALUES(1, 3);
INSERT INTO AisleContains VALUES(1, 4);
INSERT INTO AisleContains VALUES(1, 5);
INSERT INTO AisleContains VALUES(1, 6);
INSERT INTO AisleContains VALUES(1, 7);
INSERT INTO AisleContains VALUES(1, 8);
INSERT INTO AisleContains VALUES(1, 9);
INSERT INTO AisleContains VALUES(1, 10);
INSERT INTO AisleContains VALUES(1, 11);
INSERT INTO AisleContains VALUES(1, 12);
INSERT INTO AisleContains VALUES(2, 13);
INSERT INTO AisleContains VALUES(2, 14);
INSERT INTO AisleContains VALUES(2, 15);
INSERT INTO AisleContains VALUES(2, 16);
INSERT INTO AisleContains VALUES(2, 17);
INSERT INTO AisleContains VALUES(2, 18);
INSERT INTO AisleContains VALUES(2, 19);
INSERT INTO AisleContains VALUES(2, 20);
INSERT INTO AisleContains VALUES(2, 21);
INSERT INTO AisleContains VALUES(2, 22);
INSERT INTO AisleContains VALUES(2, 23);
INSERT INTO AisleContains VALUES(2, 24);
INSERT INTO AisleContains VALUES(2, 25);
INSERT INTO AisleContains VALUES(2, 26);
INSERT INTO AisleContains VALUES(2, 27);
INSERT INTO AisleContains VALUES(2, 28);
INSERT INTO AisleContains VALUES(2, 29);
INSERT INTO AisleContains VALUES(2, 30);
INSERT INTO AisleContains VALUES(2, 31);
INSERT INTO AisleContains VALUES(2, 32);
INSERT INTO AisleContains VALUES(3, 100);
INSERT INTO AisleContains VALUES(3, 101);
INSERT INTO AisleContains VALUES(3, 102);
INSERT INTO AisleContains VALUES(3, 103);
INSERT INTO AisleContains VALUES(3, 104);
INSERT INTO AisleContains VALUES(3, 105);
INSERT INTO AisleContains VALUES(3, 106);
INSERT INTO AisleContains VALUES(3, 107);
INSERT INTO AisleContains VALUES(3, 108);
INSERT INTO AisleContains VALUES(3, 109);
INSERT INTO AisleContains VALUES(3, 110);
INSERT INTO AisleContains VALUES(3, 111);
INSERT INTO AisleContains VALUES(3, 112);
INSERT INTO AisleContains VALUES(3, 113);
INSERT INTO AisleContains VALUES(3, 114);
INSERT INTO AisleContains VALUES(3, 115);
INSERT INTO AisleContains VALUES(3, 116);
INSERT INTO AisleContains VALUES(3, 117);
INSERT INTO AisleContains VALUES(3, 118);
INSERT INTO AisleContains VALUES(3, 119);
INSERT INTO AisleContains VALUES(3, 120);
INSERT INTO AisleContains VALUES(4, 150);
INSERT INTO AisleContains VALUES(4, 151);
INSERT INTO AisleContains VALUES(4, 152);
INSERT INTO AisleContains VALUES(5, 200);
INSERT INTO AisleContains VALUES(5, 201);
INSERT INTO AisleContains VALUES(5, 202);
INSERT INTO AisleContains VALUES(5, 203);
INSERT INTO AisleContains VALUES(5, 204);
INSERT INTO AisleContains VALUES(5, 205);
INSERT INTO AisleContains VALUES(5, 206);
INSERT INTO AisleContains VALUES(5, 207);
INSERT INTO AisleContains VALUES(6, 208);
INSERT INTO AisleContains VALUES(6, 209);
INSERT INTO AisleContains VALUES(6, 210);
INSERT INTO AisleContains VALUES(6, 211);
INSERT INTO AisleContains VALUES(6, 212);
INSERT INTO AisleContains VALUES(7, 300);
INSERT INTO AisleContains VALUES(7, 301);
INSERT INTO AisleContains VALUES(7, 302);
INSERT INTO AisleContains VALUES(7, 303);
INSERT INTO AisleContains VALUES(7, 304);
INSERT INTO AisleContains VALUES(7, 305);
INSERT INTO AisleContains VALUES(7, 306);
INSERT INTO AisleContains VALUES(7, 307);
INSERT INTO AisleContains VALUES(8, 400);
INSERT INTO AisleContains VALUES(8, 401);
INSERT INTO AisleContains VALUES(8, 402);
INSERT INTO AisleContains VALUES(8, 403);
INSERT INTO AisleContains VALUES(8, 404);
INSERT INTO AisleContains VALUES(8, 405);
INSERT INTO AisleContains VALUES(8, 406);
INSERT INTO AisleContains VALUES(8, 407);
INSERT INTO AisleContains VALUES(8, 408);
INSERT INTO AisleContains VALUES(8, 409);
INSERT INTO AisleContains VALUES(8, 410);
INSERT INTO AisleContains VALUES(8, 411);
INSERT INTO AisleContains VALUES(8, 412);
INSERT INTO AisleContains VALUES(8, 413);
INSERT INTO AisleContains VALUES(8, 414);
INSERT INTO AisleContains VALUES(8, 415);
INSERT INTO AisleContains VALUES(8, 416);
INSERT INTO AisleContains VALUES(8, 417);
INSERT INTO AisleContains VALUES(8, 418);
INSERT INTO AisleContains VALUES(8, 419);
INSERT INTO AisleContains VALUES(8, 420);
INSERT INTO AisleContains VALUES(8, 421);
INSERT INTO AisleContains VALUES(8, 422);
INSERT INTO AisleContains VALUES(8, 423);
INSERT INTO AisleContains VALUES(8, 424);
INSERT INTO AisleContains VALUES(8, 425);

-- insertion into ProvidedBy
INSERT INTO ProvidedBy VALUES(1,9);
INSERT INTO ProvidedBy VALUES(2,13);
INSERT INTO ProvidedBy VALUES(3,11);
INSERT INTO ProvidedBy VALUES(4,2);
INSERT INTO ProvidedBy VALUES(5,13);
INSERT INTO ProvidedBy VALUES(6,2);
INSERT INTO ProvidedBy VALUES(7,9);
INSERT INTO ProvidedBy VALUES(8,3);
INSERT INTO ProvidedBy VALUES(9,12);
INSERT INTO ProvidedBy VALUES(10,12);
INSERT INTO ProvidedBy VALUES(11,9);
INSERT INTO ProvidedBy VALUES(12,11);
INSERT INTO ProvidedBy VALUES(13,3);
INSERT INTO ProvidedBy VALUES(14,9);
INSERT INTO ProvidedBy VALUES(15,13);
INSERT INTO ProvidedBy VALUES(16,9);
INSERT INTO ProvidedBy VALUES(17,11);
INSERT INTO ProvidedBy VALUES(18,9);
INSERT INTO ProvidedBy VALUES(19,9);
INSERT INTO ProvidedBy VALUES(20,3);
INSERT INTO ProvidedBy VALUES(21,11);
INSERT INTO ProvidedBy VALUES(22,11);
INSERT INTO ProvidedBy VALUES(23,11);
INSERT INTO ProvidedBy VALUES(24,9);
INSERT INTO ProvidedBy VALUES(25,9);
INSERT INTO ProvidedBy VALUES(26,11);
INSERT INTO ProvidedBy VALUES(27,11);
INSERT INTO ProvidedBy VALUES(28,9);
INSERT INTO ProvidedBy VALUES(29,11);
INSERT INTO ProvidedBy VALUES(30,11);
INSERT INTO ProvidedBy VALUES(31,11);
INSERT INTO ProvidedBy VALUES(32,11);
INSERT INTO ProvidedBy VALUES(100,1);
INSERT INTO ProvidedBy VALUES(101,15);
INSERT INTO ProvidedBy VALUES(102,15);
INSERT INTO ProvidedBy VALUES(103,1);
INSERT INTO ProvidedBy VALUES(104,15);
INSERT INTO ProvidedBy VALUES(105,1);
INSERT INTO ProvidedBy VALUES(106,1);
INSERT INTO ProvidedBy VALUES(107,15);
INSERT INTO ProvidedBy VALUES(108,15);
INSERT INTO ProvidedBy VALUES(109,1);
INSERT INTO ProvidedBy VALUES(110,15);
INSERT INTO ProvidedBy VALUES(111,1);
INSERT INTO ProvidedBy VALUES(112,15);
INSERT INTO ProvidedBy VALUES(113,1);
INSERT INTO ProvidedBy VALUES(114,15);
INSERT INTO ProvidedBy VALUES(115,15);
INSERT INTO ProvidedBy VALUES(116,1);
INSERT INTO ProvidedBy VALUES(117,15);
INSERT INTO ProvidedBy VALUES(118,1);
INSERT INTO ProvidedBy VALUES(119,1);
INSERT INTO ProvidedBy VALUES(120,15);
INSERT INTO ProvidedBy VALUES(150,15);
INSERT INTO ProvidedBy VALUES(151,15);
INSERT INTO ProvidedBy VALUES(152,15);
INSERT INTO ProvidedBy VALUES(200,4);
INSERT INTO ProvidedBy VALUES(201,14);
INSERT INTO ProvidedBy VALUES(202,4);
INSERT INTO ProvidedBy VALUES(203,4);
INSERT INTO ProvidedBy VALUES(204,14);
INSERT INTO ProvidedBy VALUES(205,4);
INSERT INTO ProvidedBy VALUES(206,4);
INSERT INTO ProvidedBy VALUES(207,14);
INSERT INTO ProvidedBy VALUES(208,16);
INSERT INTO ProvidedBy VALUES(209,17);
INSERT INTO ProvidedBy VALUES(210,18);
INSERT INTO ProvidedBy VALUES(211,19);
INSERT INTO ProvidedBy VALUES(212,20);
INSERT INTO ProvidedBy VALUES(300,8);
INSERT INTO ProvidedBy VALUES(301,8);
INSERT INTO ProvidedBy VALUES(302,4);
INSERT INTO ProvidedBy VALUES(303,4);
INSERT INTO ProvidedBy VALUES(304,13);
INSERT INTO ProvidedBy VALUES(305,7);
INSERT INTO ProvidedBy VALUES(306,4);
INSERT INTO ProvidedBy VALUES(307,14);
INSERT INTO ProvidedBy VALUES(400,5);
INSERT INTO ProvidedBy VALUES(401,7);
INSERT INTO ProvidedBy VALUES(402,10);
INSERT INTO ProvidedBy VALUES(403,5);
INSERT INTO ProvidedBy VALUES(404,10);
INSERT INTO ProvidedBy VALUES(405,7);
INSERT INTO ProvidedBy VALUES(406,5);
INSERT INTO ProvidedBy VALUES(407,5);
INSERT INTO ProvidedBy VALUES(408,7);
INSERT INTO ProvidedBy VALUES(409,10);
INSERT INTO ProvidedBy VALUES(410,5);
INSERT INTO ProvidedBy VALUES(411,7);
INSERT INTO ProvidedBy VALUES(412,5);
INSERT INTO ProvidedBy VALUES(413,10);
INSERT INTO ProvidedBy VALUES(414,10);
INSERT INTO ProvidedBy VALUES(415,7);
INSERT INTO ProvidedBy VALUES(416,10);
INSERT INTO ProvidedBy VALUES(417,5);
INSERT INTO ProvidedBy VALUES(418,10);
INSERT INTO ProvidedBy VALUES(419,5);
INSERT INTO ProvidedBy VALUES(420,7);
INSERT INTO ProvidedBy VALUES(421,5);
INSERT INTO ProvidedBy VALUES(422,10);
INSERT INTO ProvidedBy VALUES(423,5);
INSERT INTO ProvidedBy VALUES(424,6);
INSERT INTO ProvidedBy VALUES(425,6);

-- insertion into Purchases
INSERT INTO Purchases VALUES(1, 1, 1, 1, '11-01-2017', 1.59, FALSE);
INSERT INTO Purchases VALUES(1, 17, 8, 1, '11-01-2017', 10.32, FALSE);
INSERT INTO Purchases VALUES(1, 101, 3, 1, '11-01-2017', 6.87, FALSE);
INSERT INTO Purchases VALUES(1, 113, 4, 1, '11-01-2017', 19.88, FALSE);
INSERT INTO Purchases VALUES(1, 119, 9, 1, '11-01-2017', 20.61, FALSE);
INSERT INTO Purchases VALUES(1, 201, 1, 1, '11-01-2017', 6.99, FALSE);
INSERT INTO Purchases VALUES(1, 211, 2, 1, '11-01-2017', 15.98, FALSE);
INSERT INTO Purchases VALUES(2, 307, 8, 1, '11-07-2017', 7.92, FALSE);
INSERT INTO Purchases VALUES(2, 301, 6, 1, '11-07-2017', 23.94, FALSE);
INSERT INTO Purchases VALUES(2, 421, 7, 1, '11-07-2017', 4.83, FALSE);
INSERT INTO Purchases VALUES(2, 425, 4, 1, '11-07-2017', 15.96, FALSE);
INSERT INTO Purchases VALUES(2, 3, 3, 1, '11-07-2017', 3.57, FALSE);
INSERT INTO Purchases VALUES(3, 5, 2, 2, '12-01-2017', 2.78, FALSE);
INSERT INTO Purchases VALUES(3, 7, 9, 2, '12-01-2017', 8.91, FALSE);
INSERT INTO Purchases VALUES(3, 13, 2, 2, '12-01-2017', 1.98, FALSE);
INSERT INTO Purchases VALUES(3, 17, 8, 2, '12-01-2017', 10.32, FALSE);
INSERT INTO Purchases VALUES(3, 103, 5, 2, '12-01-2017', 11.45, FALSE);
INSERT INTO Purchases VALUES(3, 115, 2, 2, '12-01-2017', 7.94, FALSE);
INSERT INTO Purchases VALUES(3, 117, 3, 2, '12-01-2017', 9.87, FALSE);
INSERT INTO Purchases VALUES(4, 203, 3, 2, '11-03-2017', 23.97, FALSE);
INSERT INTO Purchases VALUES(4, 211, 2, 2, '11-03-2017', 15.98, FALSE);
INSERT INTO Purchases VALUES(4, 305, 2, 2, '11-03-2017', 9.98, FALSE);
INSERT INTO Purchases VALUES(4, 303, 4, 2, '11-03-2017', 19.96, FALSE);
INSERT INTO Purchases VALUES(4, 414, 14, 2, '11-03-2017', 9.66, FALSE);
INSERT INTO Purchases VALUES(4, 410, 12, 2, '11-03-2017', 8.28, FALSE);
INSERT INTO Purchases VALUES(4, 7, 9, 2, '11-03-2017', 8.91, FALSE);
INSERT INTO Purchases VALUES(5, 9, 6, 3, '12-17-2017', 7.74, FALSE);
INSERT INTO Purchases VALUES(5, 21, 3, 3, '12-17-2017', 4.47, FALSE);
INSERT INTO Purchases VALUES(5, 203, 3, 3, '12-17-2017', 23.97, FALSE);
INSERT INTO Purchases VALUES(6, 301, 6, 3, '12-21-2017', 23.94, FALSE);
INSERT INTO Purchases VALUES(6, 303, 4, 3, '12-21-2017', 19.96, FALSE);
INSERT INTO Purchases VALUES(6, 402, 6, 3, '12-21-2017', 5.34, FALSE);
INSERT INTO Purchases VALUES(6, 416, 5, 3, '12-21-2017', 3.45, FALSE);
INSERT INTO Purchases VALUES(6, 7, 9, 3, '12-21-2017', 8.91, FALSE);
INSERT INTO Purchases VALUES(6, 11, 4, 3, '12-21-2017', 15.96, FALSE);
INSERT INTO Purchases VALUES(7, 13, 2, 4, '11-19-2017', 1.98, FALSE);
INSERT INTO Purchases VALUES(8, 15, 1, 4, '11-11-2017', 1.59, FALSE);
INSERT INTO Purchases VALUES(9, 17, 8, 5, '11-21-2017', 10.32, FALSE);
INSERT INTO Purchases VALUES(10, 19, 6, 5, '12-25-2017', 5.94, FALSE);
INSERT INTO Purchases VALUES(11, 21, 3, 6, '11-02-2017', 4.47, FALSE);
INSERT INTO Purchases VALUES(12, 23, 10, 6, '12-07-2017', 9.90, FALSE);
INSERT INTO Purchases VALUES(13, 25, 1, 7, '12-15-2017', 1.29, FALSE);
INSERT INTO Purchases VALUES(14, 27, 7, 7, '11-09-2017', 9.03, FALSE);
INSERT INTO Purchases VALUES(15, 29, 6, 8, '11-10-2017', 7.14, FALSE);
INSERT INTO Purchases VALUES(16, 31, 2, 8, '12-11-2017', 7.98, FALSE);
INSERT INTO Purchases VALUES(17, 101, 3, 9, '12-14-2017', 6.87, FALSE);
INSERT INTO Purchases VALUES(18, 103, 5, 9, '11-16-2017', 11.45, FALSE);
INSERT INTO Purchases VALUES(19, 105, 6, 10, '12-16-2017', 13.74, FALSE);
INSERT INTO Purchases VALUES(20, 107, 3, 10, '11-08-2017', 6.87, FALSE);
INSERT INTO Purchases VALUES(21, 109, 1, 11, '12-04-2017', 2.99, FALSE);
INSERT INTO Purchases VALUES(22, 111, 8, 11, '11-03-2017', 18.32, FALSE);
INSERT INTO Purchases VALUES(23, 113, 4, 12, '12-19-2017', 19.88, FALSE);
INSERT INTO Purchases VALUES(24, 115, 2, 12, '12-18-2017', 7.94, FALSE);
INSERT INTO Purchases VALUES(25, 117, 3, 13, '11-18-2017', 9.87, FALSE);
INSERT INTO Purchases VALUES(26, 119, 9, 13, '12-16-2017', 20.61, FALSE);
INSERT INTO Purchases VALUES(27, 150, 1, 14, '11-30-2017', 3.99, FALSE);
INSERT INTO Purchases VALUES(28, 152, 7, 14, '12-31-2017', 41.93, FALSE);
INSERT INTO Purchases VALUES(29, 201, 1, 15, '11-30-2017', 6.99, FALSE);
INSERT INTO Purchases VALUES(30, 203, 3, 15, '12-01-2017', 23.97, FALSE);
INSERT INTO Purchases VALUES(31, 205, 13, 16, '11-12-2017', 90.87, FALSE);
INSERT INTO Purchases VALUES(32, 207, 7, 16, '12-15-2017', 55.93, FALSE);
INSERT INTO Purchases VALUES(33, 209, 1, 17, '12-03-2017', 6.99, FALSE);
INSERT INTO Purchases VALUES(34, 211, 2, 17, '11-17-2017', 15.98, FALSE);
INSERT INTO Purchases VALUES(35, 301, 6, 18, '12-13-2017', 23.94, FALSE);
INSERT INTO Purchases VALUES(36, 303, 4, 18, '12-22-2017', 19.96, FALSE);
INSERT INTO Purchases VALUES(37, 305, 2, 19, '11-22-2017', 9.98, FALSE);
INSERT INTO Purchases VALUES(38, 307, 8, 19, '11-29-2017', 7.92, FALSE);
INSERT INTO Purchases VALUES(39, 401, 4, 20, '11-01-2017', 5.16, FALSE);
INSERT INTO Purchases VALUES(40, 403, 6, 20, '12-27-2017', 5.94, FALSE);
INSERT INTO Purchases VALUES(41, 405, 9, 21, '12-18-2017', 5.31, FALSE);
INSERT INTO Purchases VALUES(42, 407, 2, 21, '11-16-2017', 9.18, FALSE);
INSERT INTO Purchases VALUES(43, 409, 1, 22, '11-13-2017', 0.69, FALSE);
INSERT INTO Purchases VALUES(44, 411, 10, 22, '12-02-2017', 6.90, FALSE);
INSERT INTO Purchases VALUES(45, 413, 7, 23, '11-03-2017', 4.83, FALSE);
INSERT INTO Purchases VALUES(46, 415, 6, 23, '12-07-2017', 4.14, FALSE);
INSERT INTO Purchases VALUES(47, 417, 1, 24, '11-11-2017', 0.69, FALSE);
INSERT INTO Purchases VALUES(48, 419, 2, 24, '12-16-2017', 1.38, FALSE);
INSERT INTO Purchases VALUES(49, 421, 7, 25, '12-22-2017', 4.83, FALSE);
INSERT INTO Purchases VALUES(50, 423, 3, 25, '12-21-2017', 8.97, FALSE);
INSERT INTO Purchases VALUES(51, 425, 4, 26, '11-26-2017', 15.96, FALSE);
INSERT INTO Purchases VALUES(52, 400, 1, 26, '12-18-2017', 1.19, FALSE);
INSERT INTO Purchases VALUES(53, 402, 6, 27, '11-16-2017', 5.34, FALSE);
INSERT INTO Purchases VALUES(54, 404, 13, 27, '12-13-2017', 6.37, FALSE);
INSERT INTO Purchases VALUES(55, 406, 2, 28, '11-17-2017', 7.98, FALSE);
INSERT INTO Purchases VALUES(56, 408, 9, 28, '12-01-2017', 14.31, FALSE);
INSERT INTO Purchases VALUES(57, 410, 12, 29, '12-04-2017', 8.28, FALSE);
INSERT INTO Purchases VALUES(58, 412, 1, 29, '11-14-2017', 0.69, FALSE);
INSERT INTO Purchases VALUES(59, 414, 14, 30, '12-24-2017', 9.66, FALSE);
INSERT INTO Purchases VALUES(60, 416, 5, 30, '11-24-2017', 3.45, FALSE);


-- insertion into ProvidesDelivery
INSERT INTO ProvidesDelivery VALUES(1, 1);
INSERT INTO ProvidesDelivery VALUES(2, 1);
INSERT INTO ProvidesDelivery VALUES(3, 1);
INSERT INTO ProvidesDelivery VALUES(4, 2);
INSERT INTO ProvidesDelivery VALUES(5, 2);
INSERT INTO ProvidesDelivery VALUES(6, 2);
INSERT INTO ProvidesDelivery VALUES(7, 3);
INSERT INTO ProvidesDelivery VALUES(8, 3);
INSERT INTO ProvidesDelivery VALUES(9, 3);
INSERT INTO ProvidesDelivery VALUES(10, 4);
INSERT INTO ProvidesDelivery VALUES(11, 4);
INSERT INTO ProvidesDelivery VALUES(12, 4);
INSERT INTO ProvidesDelivery VALUES(13, 5);
INSERT INTO ProvidesDelivery VALUES(14, 5);
INSERT INTO ProvidesDelivery VALUES(15, 5);
INSERT INTO ProvidesDelivery VALUES(16, 6);
INSERT INTO ProvidesDelivery VALUES(17, 6);
INSERT INTO ProvidesDelivery VALUES(18, 6);
INSERT INTO ProvidesDelivery VALUES(19, 7);
INSERT INTO ProvidesDelivery VALUES(20, 7);
INSERT INTO ProvidesDelivery VALUES(21, 7);
INSERT INTO ProvidesDelivery VALUES(22, 8);
INSERT INTO ProvidesDelivery VALUES(23, 8);
INSERT INTO ProvidesDelivery VALUES(24, 8);
INSERT INTO ProvidesDelivery VALUES(25, 9);
INSERT INTO ProvidesDelivery VALUES(26, 9);
INSERT INTO ProvidesDelivery VALUES(27, 9);
INSERT INTO ProvidesDelivery VALUES(28, 10);
INSERT INTO ProvidesDelivery VALUES(29, 10);
INSERT INTO ProvidesDelivery VALUES(30, 10);
INSERT INTO ProvidesDelivery VALUES(31, 11);
INSERT INTO ProvidesDelivery VALUES(32, 11);
INSERT INTO ProvidesDelivery VALUES(33, 11);
INSERT INTO ProvidesDelivery VALUES(34, 12);
INSERT INTO ProvidesDelivery VALUES(35, 12);
INSERT INTO ProvidesDelivery VALUES(36, 12);
INSERT INTO ProvidesDelivery VALUES(37, 13);
INSERT INTO ProvidesDelivery VALUES(38, 13);
INSERT INTO ProvidesDelivery VALUES(39, 13);
INSERT INTO ProvidesDelivery VALUES(40, 14);
INSERT INTO ProvidesDelivery VALUES(41, 14);
INSERT INTO ProvidesDelivery VALUES(42, 14);
INSERT INTO ProvidesDelivery VALUES(43, 15);
INSERT INTO ProvidesDelivery VALUES(44, 15);
INSERT INTO ProvidesDelivery VALUES(45, 15);
INSERT INTO ProvidesDelivery VALUES(46, 16);
INSERT INTO ProvidesDelivery VALUES(47, 16);
INSERT INTO ProvidesDelivery VALUES(48, 16);
INSERT INTO ProvidesDelivery VALUES(49, 17);
INSERT INTO ProvidesDelivery VALUES(50, 17);
INSERT INTO ProvidesDelivery VALUES(51, 17);
INSERT INTO ProvidesDelivery VALUES(52, 18);
INSERT INTO ProvidesDelivery VALUES(53, 18);
INSERT INTO ProvidesDelivery VALUES(54, 18);
INSERT INTO ProvidesDelivery VALUES(55, 19);
INSERT INTO ProvidesDelivery VALUES(56, 19);
INSERT INTO ProvidesDelivery VALUES(57, 19);
INSERT INTO ProvidesDelivery VALUES(58, 20);
INSERT INTO ProvidesDelivery VALUES(59, 20);
INSERT INTO ProvidesDelivery VALUES(60, 20);

-- insertion into ReceivedFrom
INSERT INTO ReceivedFrom VALUES(1,25);
INSERT INTO ReceivedFrom VALUES(2,26);
INSERT INTO ReceivedFrom VALUES(3,31);
INSERT INTO ReceivedFrom VALUES(4,34);
INSERT INTO ReceivedFrom VALUES(5,35);
INSERT INTO ReceivedFrom VALUES(6,36);
INSERT INTO ReceivedFrom VALUES(7,27);
INSERT INTO ReceivedFrom VALUES(8,32);
INSERT INTO ReceivedFrom VALUES(9,34);
INSERT INTO ReceivedFrom VALUES(10,35);
INSERT INTO ReceivedFrom VALUES(11,25);
INSERT INTO ReceivedFrom VALUES(12,33);
INSERT INTO ReceivedFrom VALUES(13,31);
INSERT INTO ReceivedFrom VALUES(14,26);
INSERT INTO ReceivedFrom VALUES(15,32);
INSERT INTO ReceivedFrom VALUES(16,27);
INSERT INTO ReceivedFrom VALUES(17,33);
INSERT INTO ReceivedFrom VALUES(18,25);
INSERT INTO ReceivedFrom VALUES(19,26);
INSERT INTO ReceivedFrom VALUES(20,31);
INSERT INTO ReceivedFrom VALUES(21,32);
INSERT INTO ReceivedFrom VALUES(22,33);
INSERT INTO ReceivedFrom VALUES(23,31);
INSERT INTO ReceivedFrom VALUES(24,27);
INSERT INTO ReceivedFrom VALUES(25,25);
INSERT INTO ReceivedFrom VALUES(26,32);
INSERT INTO ReceivedFrom VALUES(27,33);
INSERT INTO ReceivedFrom VALUES(28,26);
INSERT INTO ReceivedFrom VALUES(29,31);
INSERT INTO ReceivedFrom VALUES(30,32);
INSERT INTO ReceivedFrom VALUES(31,33);
INSERT INTO ReceivedFrom VALUES(32,31);
INSERT INTO ReceivedFrom VALUES(100,1);
INSERT INTO ReceivedFrom VALUES(101,43);
INSERT INTO ReceivedFrom VALUES(102,44);
INSERT INTO ReceivedFrom VALUES(103,2);
INSERT INTO ReceivedFrom VALUES(104,45);
INSERT INTO ReceivedFrom VALUES(105,3);
INSERT INTO ReceivedFrom VALUES(106,1);
INSERT INTO ReceivedFrom VALUES(107,43);
INSERT INTO ReceivedFrom VALUES(108,44);
INSERT INTO ReceivedFrom VALUES(109,2);
INSERT INTO ReceivedFrom VALUES(110,45);
INSERT INTO ReceivedFrom VALUES(111,3);
INSERT INTO ReceivedFrom VALUES(112,43);
INSERT INTO ReceivedFrom VALUES(113,1);
INSERT INTO ReceivedFrom VALUES(114,44);
INSERT INTO ReceivedFrom VALUES(115,45);
INSERT INTO ReceivedFrom VALUES(116,2);
INSERT INTO ReceivedFrom VALUES(117,43);
INSERT INTO ReceivedFrom VALUES(118,3);
INSERT INTO ReceivedFrom VALUES(119,1);
INSERT INTO ReceivedFrom VALUES(120,44);
INSERT INTO ReceivedFrom VALUES(150,45);
INSERT INTO ReceivedFrom VALUES(151,43);
INSERT INTO ReceivedFrom VALUES(152,44);
INSERT INTO ReceivedFrom VALUES(200,10);
INSERT INTO ReceivedFrom VALUES(201,40);
INSERT INTO ReceivedFrom VALUES(202,11);
INSERT INTO ReceivedFrom VALUES(203,12);
INSERT INTO ReceivedFrom VALUES(204,41);
INSERT INTO ReceivedFrom VALUES(205,10);
INSERT INTO ReceivedFrom VALUES(206,11);
INSERT INTO ReceivedFrom VALUES(207,42);
INSERT INTO ReceivedFrom VALUES(208,46);
INSERT INTO ReceivedFrom VALUES(209,50);
INSERT INTO ReceivedFrom VALUES(210,53);
INSERT INTO ReceivedFrom VALUES(211,56);
INSERT INTO ReceivedFrom VALUES(212,59);
INSERT INTO ReceivedFrom VALUES(400,13);
INSERT INTO ReceivedFrom VALUES(401,19);
INSERT INTO ReceivedFrom VALUES(402,28);
INSERT INTO ReceivedFrom VALUES(403,14);
INSERT INTO ReceivedFrom VALUES(404,29);
INSERT INTO ReceivedFrom VALUES(405,20);
INSERT INTO ReceivedFrom VALUES(406,15);
INSERT INTO ReceivedFrom VALUES(407,13);
INSERT INTO ReceivedFrom VALUES(408,21);
INSERT INTO ReceivedFrom VALUES(409,30);
INSERT INTO ReceivedFrom VALUES(410,14);
INSERT INTO ReceivedFrom VALUES(411,19);
INSERT INTO ReceivedFrom VALUES(412,15);
INSERT INTO ReceivedFrom VALUES(413,28);
INSERT INTO ReceivedFrom VALUES(414,29);
INSERT INTO ReceivedFrom VALUES(415,20);
INSERT INTO ReceivedFrom VALUES(416,30);
INSERT INTO ReceivedFrom VALUES(417,13);
INSERT INTO ReceivedFrom VALUES(418,28);
INSERT INTO ReceivedFrom VALUES(419,14);
INSERT INTO ReceivedFrom VALUES(420,21);
INSERT INTO ReceivedFrom VALUES(421,15);
INSERT INTO ReceivedFrom VALUES(422,29);
INSERT INTO ReceivedFrom VALUES(423,13);
INSERT INTO ReceivedFrom VALUES(424,30);
INSERT INTO ReceivedFrom VALUES(425,19);
