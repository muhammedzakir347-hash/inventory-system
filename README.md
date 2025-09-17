Inventory Management System
A Python-based Inventory Management System using SQLite3, Tabulate, and CSV Export. This system supports role-based access, CRUD operations for suppliers, products, customers, sales, and report generation.
 
Features
User Authentication
•	Login system with username and password.
•	Role-based permissions:
o	Admin: Full access to all modules.
o	Salesperson: Can view all data, manage customers and sales, and export reports.
Supplier Management
•	View, search, add, update, and delete suppliers.
•	Each supplier has a unique ID prefix (e.g., SP_1, SP_2).
Product Management
•	View, add, update, and delete products.
•	Each product has a unique ID prefix (e.g., PR_1, PR_2).
•	Stock tracking with automatic quantity updates after sales.
Customer Management
•	View, add, update, and delete customers.
•	Each customer has a unique ID prefix (e.g., CU_1, CU_2).
Sales Management
•	Add sales with multiple products in a single sale.
•	Customer ID is asked only once per sale.
•	Each sale has a unique ID prefix (e.g., SL_1, SL_2).
•	Updates product stock automatically.
•	View, update, and delete sales records.
•	Export sales reports to CSV.
Reports
•	Stock Report: Displays product inventory with current quantities.
•	Sales Report: Shows all sales transactions with product and customer details.
•	Supplier Report: Lists suppliers with their products.
•	CSV export functionality for all reports.
Role Permissions
•	Admin: Full CRUD and report access.
•	Salesperson: View all, full access to customers and sales, export reports.
Logout & Login Loop
•	Users can logout, returning to the login screen.
•	Multiple users can log in without restarting the program.
 
Technologies Used
•	Python 3.x
•	SQLite3 (for database)
•	Tabulate (for pretty table output)
•	CSV (for exporting reports)
 
Installation
1.	Clone the repository:
2.	git clone <muhammedzakir347-hash/inventory-system>
3.	Install dependencies:
4.	pip install tabulate
5.	Run the program:
6.	python workinginman.py
 
Usage
1.	Login using credentials:
o	Admin: username=admin, password=admin123
o	Salesperson: username=sales, password=sales123
2.	Navigate through the Main Menu:
o	1. Suppliers → Manage supplier records.
o	2. Products → Manage products, update stock, and check availability.
o	3. Customers → Add, edit, delete, or view customer details.
o	4. Sales → Add sales (multi-product), update, delete, or view past sales.
o	5. Reports → Generate stock, sales, or supplier reports.
o	6. Logout → Return to the login screen.
3.	Sales Workflow:
o	Enter customer ID once per sale.
o	Select multiple products by ID and quantity.
o	The system will display product details (name, stock, price) before confirmation.
o	Stock levels update automatically after confirming the sale.
4.	Reports:
o	Choose a report type (Stock, Sales, Supplier).
o	Data is displayed in a formatted table.
o	Option to export to CSV for external use.
 
Demo Workflow (Example)
Step 1: Login
Username: admin
Password: admin123
Step 2: Main Menu
1. Suppliers
2. Products
3. Customers
4. Sales
5. Reports
6. Logout
Step 3: Add a Product
> 2 (Products)
> 2 (Add Product)
Name: Orrenge
Category: Fruits
Size: 500 gm
Quantity: 300
Price: 50
Supplier ID: SP_2
✅ Product added.
Step 4: Add a Customer
> 3 (Customers)
> 2 (Add Customer)
Enter customer name: John Doe
Enter phone: 1234567890
Customer added with ID: CU_1
Step 5: Make a Sale
> 4 (Sales)
> 1 (Add Sale)
Customer ID: CU_1
Product ID: PR_1
Product: Apple, Price: 40.5, Stock: 300
Quantity: 12
Add another product to this sale? (y/n): y
Product ID: PR_2
Product: Mango Juice, Price: 10.5, Stock: 200
Quantity: 50
Add another product to this sale? (y/n): n

=== Confirm Sales ===
+-----------+--------------+-------+---------+---------------------+
| Sale ID   | Product ID   |   Qty |   Total | Date                |
+===========+==============+=======+=========+=====================+
| SL_1      | PR_1         |    12 |     486 | 2025-09-17 09:43:58 |
+-----------+--------------+-------+---------+---------------------+
| SL_2      | PR_2         |    50 |     525 | 2025-09-17 09:44:54 |
+-----------+--------------+-------+---------+---------------------+
Confirm all sales? (y/n):
✅ Sale(s) recorded.
Step 6: Generate Reports
> 5 (Reports)
> 1 (Stock Report)
Enter choice: 1
+--------------+-------------+-------+
| Product ID   | Name        |   Qty |
+==============+=============+=======+
| PR_1         | Apple       |   288 |
+--------------+-------------+-------+
| PR_2         | Mango Juice |   150 |
+--------------+-------------+-------+
| PR_3         | Orrenge     |   300 |
+--------------+-------------+-------+
Export this report to CSV? (y/n): 
✅ Exported to stock_report_20250917_094708.csv
Step 7: Logout
> 6 (Logout)
Returning to login screen...
 
Database
•	Stored in inventory.db
•	Tables:
o	users: Stores user credentials and roles.
o	suppliers: Supplier information (with unique SP_ prefixed IDs).
o	products: Product inventory (with unique PR_ prefixed IDs).
o	customers: Customer information (with unique CU_ prefixed IDs).
o	sales: Sales transactions (with unique SL_ prefixed IDs).
 Extra Features added
•	Role-based Access Control (Admin vs. Salesperson).
•	Unique ID Prefix System (SP_, PR_, CU_, SA_) for clarity.
•	Auto Stock Management (product quantity decreases after sales).
•	Advanced Sales System: one customer ID per sale, multiple products in a single transaction.
•	Report Exporting: sales, stock, suppliers → CSV.
•	Enhanced CLI Experience with logout/login loop (multi-user session without restarting).
•	Tabular Display using tabulate for professional look.

