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
Product Management
•	View, add, update, and delete products.
•	Stock tracking with automatic quantity updates after sales.
Customer Management
•	View, add, update, and delete customers.
Sales Management
•	Add sales with multiple products in a single sale.
•	Ask for customer ID only once per sale.
•	Updates product stock automatically.
•	View, update, and delete sales records.
•	Export sales reports to CSV.
Reports
•	Stock Report
•	Sales Report
•	Supplier Report
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
Usage
1.	Login using credentials:
o	Admin: username=admin, password=admin123
o	Salesperson: username=sales, password=sales123
2.	Navigate through the Main Menu:
o	Suppliers, Products, Customers, Sales, Reports
o	Use numbers to select menu options.
3.	Logout anytime to return to the login screen.
<img width="468" height="171" alt="image" src="https://github.com/user-attachments/assets/741a52c2-8cf4-4cf3-af86-8e812bd071f9" />


<img width="468" height="620" alt="image" src="https://github.com/user-attachments/assets/2da5946f-dda2-4e6d-9df2-04fbebe35fd7" />
