
import sqlite3
import os
import getpass
from datetime import datetime
from tabulate import tabulate
import csv

DB_NAME = "inventory.db"

# -------------------- Helpers --------------------
def pause():
    input("\nPress Enter to continue...")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_table(data, headers):
    if data:
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("\nNo records found.\n")

def print_menu(title, options):
    table_data = [[i, opt] for i, opt in enumerate(options)]
    print("\n" + title)
    print(tabulate(table_data, headers=["Option", "Description"], tablefmt="grid"))

def get_nonempty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("❌ Input cannot be blank. Try again.")

def generate_id(table, prefix, col):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT {col} FROM {table} ORDER BY ROWID DESC LIMIT 1")
        last = cur.fetchone()
    except sqlite3.OperationalError:
        last = None
    conn.close()
    if last and last[0]:
        try:
            num = int(last[0].split("_")[1]) + 1
        except:
            num = 1
    else:
        num = 1
    return f"{prefix}_{num}"

def export_to_csv(filename, headers, rows=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if rows is None:
        cur.execute(f"SELECT * FROM {filename}")
        rows = cur.fetchall()
    conn.close()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{filename}_{ts}.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"✅ Exported to {file_path}")

# -------------------- Database Init --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Users
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT)""")
    # Suppliers
    cur.execute("""CREATE TABLE IF NOT EXISTS suppliers(
                    supplier_id TEXT PRIMARY KEY,
                    name TEXT,
                    contact TEXT,
                    address TEXT)""")
    # Products
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
                    product_id TEXT PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    size TEXT,
                    quantity INTEGER,
                    price REAL,
                    supplier_id TEXT,
                    FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id))""")
    # Customers
    cur.execute("""CREATE TABLE IF NOT EXISTS customers(
                    customer_id TEXT PRIMARY KEY,
                    name TEXT,
                    contact TEXT)""")
    # Sales
    cur.execute("""CREATE TABLE IF NOT EXISTS sales(
                    sale_id TEXT PRIMARY KEY,
                    product_id TEXT,
                    customer_id TEXT,
                    quantity INTEGER,
                    total REAL,
                    date TEXT,
                    FOREIGN KEY(product_id) REFERENCES products(product_id),
                    FOREIGN KEY(customer_id) REFERENCES customers(customer_id))""")
    # Default users
    cur.execute("SELECT * FROM users")
    if not cur.fetchall():
        cur.execute("INSERT INTO users VALUES(?,?,?,?)",
                    ("U_1", "admin", "admin123", "admin"))
        cur.execute("INSERT INTO users VALUES(?,?,?,?)",
                    ("U_2", "sales", "sales123", "salesperson"))
    conn.commit()
    conn.close()

# -------------------- Authentication --------------------
def login():
    clear_screen()
    print("=== Login ===")
    username = get_nonempty_input("Username: ")
    password = getpass.getpass("Password: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return row
    else:
        print("❌ Invalid credentials.")
        pause()
        return None

# -------------------- Supplier CRUD --------------------
def view_suppliers():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers")
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Supplier ID", "Name", "Contact", "Address"])
    pause()

def search_supplier():
    name = get_nonempty_input("Enter name to search: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers WHERE name LIKE ?", (f"%{name}%",))
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Supplier ID", "Name", "Contact", "Address"])
    pause()

def add_supplier():
    sid = generate_id("suppliers", "SP", "supplier_id")
    name = get_nonempty_input("Name: ")
    contact = get_nonempty_input("Contact: ")
    address = get_nonempty_input("Address: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO suppliers VALUES(?,?,?,?)", (sid, name, contact, address))
    conn.commit()
    conn.close()
    print("✅ Supplier added.")
    pause()

def update_supplier():
    sid = get_nonempty_input("Supplier ID to update: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers WHERE supplier_id=?", (sid,))
    row = cur.fetchone()
    if not row:
        print("❌ Supplier not found.")
        conn.close()
        pause()
        return
    print("\nCurrent details:")
    print(f"Name    : {row[1]}")
    print(f"Contact : {row[2]}")
    print(f"Address : {row[3]}")
    name = input(f"New name (blank='{row[1]}'): ").strip() or row[1]
    contact = input(f"New contact (blank='{row[2]}'): ").strip() or row[2]
    address = input(f"New address (blank='{row[3]}'): ").strip() or row[3]
    cur.execute("UPDATE suppliers SET name=?, contact=?, address=? WHERE supplier_id=?",
                (name, contact, address, sid))
    conn.commit()
    conn.close()
    print("✅ Supplier updated.")
    pause()

def delete_supplier():
    sid = get_nonempty_input("Supplier ID to delete: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM suppliers WHERE supplier_id=?", (sid,))
    conn.commit()
    conn.close()
    print("✅ Supplier deleted (if existed).")
    pause()

# -------------------- Product CRUD --------------------
def view_products():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Product ID", "Name", "Category", "Size", "Qty", "Price", "Supplier ID"])
    pause()

def add_product():
    pid = generate_id("products", "PR", "product_id")
    name = get_nonempty_input("Name: ")
    category = get_nonempty_input("Category: ")
    size = get_nonempty_input("Size: ")
    quantity = int(get_nonempty_input("Quantity: "))
    price = float(get_nonempty_input("Price: "))
    supplier_id = get_nonempty_input("Supplier ID: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO products VALUES(?,?,?,?,?,?,?)",
                (pid, name, category, size, quantity, price, supplier_id))
    conn.commit()
    conn.close()
    print("✅ Product added.")
    pause()

def update_product():
    pid = get_nonempty_input("Product ID to update: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE product_id=?", (pid,))
    row = cur.fetchone()
    if not row:
        print("❌ Product not found.")
        conn.close()
        pause()
        return
    print("\nCurrent details:")
    print(f"Name:{row[1]}, Category:{row[2]}, Size:{row[3]}, Qty:{row[4]}, Price:{row[5]}, Supplier:{row[6]}")
    name = input(f"New name (blank='{row[1]}'): ").strip() or row[1]
    category = input(f"New category (blank='{row[2]}'): ").strip() or row[2]
    size = input(f"New size (blank='{row[3]}'): ").strip() or row[3]
    quantity = input(f"New quantity (blank='{row[4]}'): ").strip() or row[4]
    price = input(f"New price (blank='{row[5]}'): ").strip() or row[5]
    supplier_id = input(f"New supplier_id (blank='{row[6]}'): ").strip() or row[6]
    cur.execute("UPDATE products SET name=?, category=?, size=?, quantity=?, price=?, supplier_id=? WHERE product_id=?",
                (name, category, size, quantity, price, supplier_id, pid))
    conn.commit()
    conn.close()
    print("✅ Product updated.")
    pause()

def delete_product():
    pid = get_nonempty_input("Product ID to delete: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE product_id=?", (pid,))
    conn.commit()
    conn.close()
    print("✅ Product deleted (if existed).")
    pause()

# -------------------- Customer CRUD --------------------
def view_customers():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Customer ID", "Name", "Contact"])
    pause()

def add_customer():
    cid = generate_id("customers", "CU", "customer_id")
    name = get_nonempty_input("Name: ")
    contact = get_nonempty_input("Contact: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO customers VALUES(?,?,?)", (cid, name, contact))
    conn.commit()
    conn.close()
    print("✅ Customer added.")
    pause()

def update_customer():
    cid = get_nonempty_input("Customer ID to update: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id=?", (cid,))
    row = cur.fetchone()
    if not row:
        print("❌ Customer not found.")
        conn.close()
        pause()
        return
    print("\nCurrent details:")
    print(f"Name:{row[1]}, Contact:{row[2]}")
    name = input(f"New name (blank='{row[1]}'): ").strip() or row[1]
    contact = input(f"New contact (blank='{row[2]}'): ").strip() or row[2]
    cur.execute("UPDATE customers SET name=?, contact=? WHERE customer_id=?",
                (name, contact, cid))
    conn.commit()
    conn.close()
    print("✅ Customer updated.")
    pause()

def delete_customer():
    cid = get_nonempty_input("Customer ID to delete: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM customers WHERE customer_id=?", (cid,))
    conn.commit()
    conn.close()
    print("✅ Customer deleted (if existed).")
    pause()

# -------------------- Sales CRUD --------------------
def view_sales():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Sale ID", "Product ID", "Customer ID", "Qty", "Total", "Date"])
    pause()

def add_sale():
    sales_list = []

    # Ask customer once
    customer_id = get_nonempty_input("Customer ID: ")

    # Get last sale number from DB
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT sale_id FROM sales ORDER BY ROWID DESC LIMIT 1")
    last = cur.fetchone()
    conn.close()
    if last and last[0]:
        try:
            last_num = int(last[0].split("_")[1])
        except:
            last_num = 0
    else:
        last_num = 0

    sale_counter = last_num + 1

    while True:
        product_id = get_nonempty_input("Product ID: ")

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT name, price, quantity FROM products WHERE product_id=?", (product_id,))
        row = cur.fetchone()
        if not row:
            print("❌ Product not found.")
            conn.close()
            continue
        name, price, stock = row
        print(f"Product: {name}, Price: {price}, Stock: {stock}")

        quantity = int(get_nonempty_input("Quantity: "))
        if quantity > stock:
            print("❌ Not enough stock.")
            conn.close()
            continue

        total = price * quantity
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Generate unique sale ID in memory
        sid = f"SL_{sale_counter}"
        sale_counter += 1

        sales_list.append({"sale_id": sid, "product_id": product_id, "customer_id": customer_id,
                           "qty": quantity, "total": total, "date": date})
        conn.close()

        more = input("Add another product to this sale? (y/n): ").strip().lower()
        if more != "y":
            break

    # Show confirmation list
    print("\n=== Confirm Sales ===")
    table_data = [[s["sale_id"], s["product_id"], s["qty"], s["total"], s["date"]] for s in sales_list]
    print_table(table_data, ["Sale ID", "Product ID", "Qty", "Total", "Date"])
    confirm = input("Confirm all sales? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Sale cancelled.")
        pause()
        return

    # Insert into DB
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for s in sales_list:
        cur.execute("INSERT INTO sales VALUES(?,?,?,?,?,?)",
                    (s["sale_id"], s["product_id"], s["customer_id"], s["qty"], s["total"], s["date"]))
        cur.execute("UPDATE products SET quantity = quantity - ? WHERE product_id=?", (s["qty"], s["product_id"]))
    conn.commit()
    conn.close()
    print("✅ Sale(s) recorded.")
    pause()

def update_sale():
    sid = get_nonempty_input("Sale ID to update: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales WHERE sale_id=?", (sid,))
    row = cur.fetchone()
    if not row:
        print("❌ Sale not found.")
        conn.close()
        pause()
        return
    print("\nCurrent details:")
    print(f"Product:{row[1]}, Customer:{row[2]}, Qty:{row[3]}, Total:{row[4]}, Date:{row[5]}")
    product_id = input(f"New product_id (blank='{row[1]}'): ").strip() or row[1]
    customer_id = input(f"New customer_id (blank='{row[2]}'): ").strip() or row[2]
    quantity = input(f"New quantity (blank='{row[3]}'): ").strip() or row[3]
    total = input(f"New total (blank='{row[4]}'): ").strip() or row[4]
    date = input(f"New date (blank='{row[5]}'): ").strip() or row[5]
    cur.execute("UPDATE sales SET product_id=?, customer_id=?, quantity=?, total=?, date=? WHERE sale_id=?",
                (product_id, customer_id, quantity, total, date, sid))
    conn.commit()
    conn.close()
    print("✅ Sale updated.")
    pause()

def delete_sale():
    sid = get_nonempty_input("Sale ID to delete: ")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM sales WHERE sale_id=?", (sid,))
    conn.commit()
    conn.close()
    print("✅ Sale deleted (if existed).")
    pause()

# -------------------- Reports --------------------
def stock_report():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT product_id, name, quantity FROM products")
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Product ID", "Name", "Qty"])
    export = input("Export this report to CSV? (y/n): ").strip().lower()
    if export == "y":
        export_to_csv("stock_report", ["Product ID", "Name", "Qty"], rows)
    pause()

def sales_report():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT sale_id, product_id, customer_id, quantity, total, date FROM sales")
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Sale ID", "Product", "Customer", "Qty", "Total", "Date"])
    export = input("Export this report to CSV? (y/n): ").strip().lower()
    if export == "y":
        export_to_csv("sales_report", ["Sale ID", "Product", "Customer", "Qty", "Total", "Date"], rows)
    pause()

def supplier_report():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT s.supplier_id, s.name, IFNULL(p.name, '-') AS product_name, IFNULL(p.quantity, 0) AS qty
        FROM suppliers s
        LEFT JOIN products p ON s.supplier_id = p.supplier_id
        ORDER BY s.name
    """)
    rows = cur.fetchall()
    conn.close()
    print_table(rows, ["Supplier ID", "Supplier Name", "Product", "Qty"])
    export = input("Export this report to CSV? (y/n): ").strip().lower()
    if export == "y":
        export_to_csv("supplier_report", ["Supplier ID", "Supplier Name", "Product", "Qty"], rows)
    pause()

# -------------------- Menus --------------------
def supplier_menu():
    while True:
        clear_screen()
        print_menu("Manage Suppliers ---", [
            "Back", "View Suppliers", "Search Supplier by Name",
            "Add Supplier", "Update Supplier", "Delete Supplier"
        ])
        ch = input("Enter choice: ").strip()
        if ch == "0": break
        elif ch == "1": view_suppliers()
        elif ch == "2": search_supplier()
        elif ch == "3": add_supplier()
        elif ch == "4": update_supplier()
        elif ch == "5": delete_supplier()

def product_menu():
    while True:
        clear_screen()
        print_menu("Manage Products ---", [
            "Back", "View Products", "Add Product", "Update Product", "Delete Product"
        ])
        ch = input("Enter choice: ").strip()
        if ch == "0": break
        elif ch == "1": view_products()
        elif ch == "2": add_product()
        elif ch == "3": update_product()
        elif ch == "4": delete_product()

def customer_menu():
    while True:
        clear_screen()
        print_menu("Manage Customers ---", [
            "Back", "View Customers", "Add Customer", "Update Customer", "Delete Customer"
        ])
        ch = input("Enter choice: ").strip()
        if ch == "0": break
        elif ch == "1": view_customers()
        elif ch == "2": add_customer()
        elif ch == "3": update_customer()
        elif ch == "4": delete_customer()

def sales_menu():
    while True:
        clear_screen()
        print_menu("Sales Menu ---", [
            "Back", "Add Sale", "View Sales", "Update Sale", "Delete Sale"
        ])
        ch = input("Enter choice: ").strip()
        if ch == "0": break
        elif ch == "1": add_sale()
        elif ch == "2": view_sales()
        elif ch == "3": update_sale()
        elif ch == "4": delete_sale()

def reports_menu():
    while True:
        clear_screen()
        print_menu("Reports Menu ---", [
            "Back", "Stock Report", "Sales Report", "Supplier Report"
        ])
        ch = input("Enter choice: ").strip()
        if ch == "0": break
        elif ch == "1": stock_report()
        elif ch == "2": sales_report()
        elif ch == "3": supplier_report()

def main_menu(user):
    role = user[3]  # admin or salesperson
    while True:
        clear_screen()
        print(f"Logged in as: {user[1]} ({role})")
        # Change Exit to Logout
        menu_options = ["Logout"]

        if role == "admin":
            menu_options += ["Suppliers", "Products", "Customers", "Sales", "Reports"]
        elif role == "salesperson":
            menu_options += ["Suppliers (View Only)", "Products (View Only)", "Customers", "Sales", "Reports"]

        print_menu("Main Menu ---", menu_options)
        ch = input("Enter choice: ").strip()

        # Logout
        if ch == "0":
            break

        # Admin full access
        if role == "admin":
            if ch == "1": supplier_menu()
            elif ch == "2": product_menu()
            elif ch == "3": customer_menu()
            elif ch == "4": sales_menu()
            elif ch == "5": reports_menu()
        # Salesperson limited access
        elif role == "salesperson":
            if ch == "1":
                # View suppliers only
                clear_screen()
                view_suppliers()
            elif ch == "2":
                # View products only
                clear_screen()
                view_products()
            elif ch == "3":
                customer_menu()  # full access
            elif ch == "4":
                sales_menu()  # full access
            elif ch == "5":
                reports_menu()  # full access (with export)

# -------------------- Program Start --------------------
if __name__ == "__main__":
    init_db()
    while True:
        user = login()
        if user:
            main_menu(user)
        else:
            # If login fails, ask again
            continue
