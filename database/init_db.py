import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "database/data.db"

# Make dataset reproducible
random.seed(42)


# ===============================
# TABLE CREATION
# ===============================

def create_tables(cursor):

    cursor.execute("DROP TABLE IF EXISTS order_items;")
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("DROP TABLE IF EXISTS customers;")

    cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        signup_date DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        category TEXT,
        price REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date DATE,
        total_amount REAL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    """)


# ===============================
# SEED DATA
# ===============================

def seed_customers(cursor):
    cities = ["Chennai", "Hyderabad", "Bangalore", "Mumbai", "Delhi"]

    for i in range(50):
        cursor.execute("""
        INSERT INTO customers (name, city, signup_date)
        VALUES (?, ?, ?)
        """, (
            f"Customer_{i+1}",
            cities[i % len(cities)],
            datetime(2022, 1, 1) + timedelta(days=i * 5)
        ))


def seed_products(cursor):
    products = [
        ("Laptop", "Electronics", 70000),
        ("Phone", "Electronics", 30000),
        ("Headphones", "Electronics", 5000),
        ("Shoes", "Fashion", 4000),
        ("T-shirt", "Fashion", 1200),
        ("Watch", "Accessories", 8000),
        ("Tablet", "Electronics", 45000),
        ("Backpack", "Accessories", 3500)
    ]

    cursor.executemany("""
    INSERT INTO products (product_name, category, price)
    VALUES (?, ?, ?)
    """, products)


def seed_orders_and_items(cursor):

    for order_index in range(200):

        customer_id = (order_index % 50) + 1
        order_date = datetime(2023, 1, 1) + timedelta(days=order_index)

        # Insert order first with dummy total
        cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (?, ?, ?)
        """, (customer_id, order_date, 0))

        order_id = cursor.lastrowid

        total_amount = 0

        # Add 1–3 items per order
        for _ in range((order_index % 3) + 1):

            product_id = random.randint(1, 8)
            quantity = random.randint(1, 4)

            cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity)
            VALUES (?, ?, ?)
            """, (order_id, product_id, quantity))

            # Fetch product price
            cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
            price = cursor.fetchone()[0]

            total_amount += price * quantity

        # Update total_amount properly
        cursor.execute("""
        UPDATE orders
        SET total_amount = ?
        WHERE order_id = ?
        """, (total_amount, order_id))


# ===============================
# INIT DB
# ===============================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Creating tables...")
    create_tables(cursor)

    print("Seeding customers...")
    seed_customers(cursor)

    print("Seeding products...")
    seed_products(cursor)

    print("Seeding orders and order items...")
    seed_orders_and_items(cursor)

    conn.commit()
    conn.close()

    print(f"Database '{DB_NAME}' created successfully!")


if __name__ == "__main__":
    init_db()