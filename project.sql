USE project;
 Drop TABLES  rack;
  SHOW TABLES;
DROP database project;
CREATE DATABASE project;


 CREATE TABLE Inventory
 (product_id VARCHAR(10) PRIMARY KEY,
  product_name VARCHAR(25),
  product_company VARCHAR(20),
  Quantity INT);
  
CREATE TABLE supplier
(supplier_id VARCHAR(10) PRIMARY KEY,
 supplier_name VARCHAR(50),
 contact_no  VARCHAR(11),
 email_id  VARCHAR(30),
 product_id VARCHAR(10),
 Address VARCHAR(50),
 foreign key (product_id) references Inventory(product_id));
 
CREATE TABLE Offers
( Offer_id VARCHAR(10) primary KEY,
  Offer_des VARCHAR(30),
  Offer  DECIMAL(2,2),
  Start_date DATE,
  End_date  DATE,
  product_id VARCHAR(10),
  foreign key(product_id) references Inventory(product_id));
  
 CREATE TABLE EMPLOYEE
 ( Emp_id VARCHAR(10) primary key,
   Fname  varchar(10),
   Lname  VARCHAR(10),
   email_id VARCHAR(50),
   contact_no VARCHAR(11),
   Address  VARCHAR(50),
   Salary  INT,
   Join_date DATE);
 
  CREATE TABLE Sales
 ( sale_id VARCHAR(10),
   product_id VARCHAR(10),
   product_name VARCHAR(25),
   sale_price  float NOT NULL,
   status  VARCHAR(10),
   PRIMARY KEY (sale_id,product_id));
 
 CREATE TABLE Orders
 ( Order_id VARCHAR(10) PRIMARY KEY,
   customer_name VARCHAR(20) NOT NULL,
   contact_no VARCHAR(11) NOT NULL,
   Address    VARCHAR(50) NOT NULL,
   product_id VARCHAR(10),
   sale_price float NOT NULL,
   Order_date		DATE NOT NULL,
   status varchar(10),
   foreign key(product_id) references Inventory(product_id));
 
  CREATE TABLE Custormer
  ( Custormer_id VARCHAR(10) PRIMARY KEY,
	Fname	VARCHAR(10) NOT NULL,
    contact_no VARCHAR(11) NOT NULL,
    Address		VARCHAR(50));

CREATE TABLE shipping
( shipping_id	VARCHAR(10) PRIMARY KEY,
	Order_id	Varchar(10)	NOT NULL,
    Address	VARCHAR(50)	 NOT NULL,
    dis_date 		DATE NOT NULL,
    Order_date		DATE NOT NULL,
    foreign key (Order_id) references Orders(Order_id));
  
CREATE TABLE rack
(Rack_id VARCHAR(10) NOT NULL,
 Capacity INT NOT NULL,
 stock	  INT,
  Last_up	TIME);
  
  INSERT INTO Inventory (product_id, product_name, product_company, Quantity) VALUES
('P001', 'Laptop', 'Dell', 50),
('P002', 'Smartphone', 'Apple', 100),
('P003', 'Tablet', 'Samsung', 75);

INSERT INTO supplier (supplier_id, supplier_name, contact_no, email_id, product_id, Address) VALUES
('S001', 'Tech Supplies', '1234567890', 'techsupplies@example.com', 'P001', '123 Tech Lane'),
('S002', 'Gadgets Inc.', '0987654321', 'gadgets@example.com', 'P002', '456 Gadget Ave'),
('S003', 'Mobile World', '1122334455', 'mobileworld@example.com', 'P003', '789 Mobile St');

INSERT INTO Offers (Offer_id, Offer_des, Offer, Start_date, End_date, product_id) VALUES
('O001', '10% off on Laptops', 0.10, '2023-01-01', '2023-01-31', 'P001'),
('O002', '5% off on Smartphones', 0.05, '2023-02-01', '2023-02-28', 'P002'),
('O003', '15% off on Tablets', 0.15, '2023-03-01', '2023-03-31', 'P003');

INSERT INTO EMPLOYEE (Emp_id, Fname, Lname, email_id, contact_no, Address, Salary, Join_date) VALUES
('E001', 'John', 'Doe', 'john.doe@example.com', '1234567890', '101 Main St', 50000, '2022-01-15'),
('E002', 'Jane', 'Smith', 'jane.smith@example.com', '0987654321', '202 Second St', 60000, '2022-02-20'),
('E003', 'Alice', 'Johnson', 'alice.johnson@example.com', '1122334455', '303 Third St', 55000, '2022-03-25');

INSERT INTO Orders (Order_id, customer_name, contact_no, Address, product_id, sale_price, Order_date, status) VALUES
('O001', 'Michael Brown', '1234567890', '404 Fourth St', 'P001', 800.00, '2023-01-10', 'Shipped'),
('O002', 'Emily Davis', '0987654321', '505 Fifth St', 'P002', 999.99, '2023-02-15', 'Processing'),
('O003', 'David Wilson', '1122334455', '606 Sixth St', 'P003', 300.00, '2023-03-20', 'Delivered');

INSERT INTO shipping (shipping_id, Order_id, Address, dis_date, Order_date) VALUES
('SH001', 'O001', '404 Fourth St', '2023-01-12', '2023-01-10'),
('SH002', 'O002', '505 Fifth St', '2023-02-18', '2023-02-15'),
('SH003', 'O003', '606 Sixth St', '2023-03-22', '2023-03-20');