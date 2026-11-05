
import sqlite3

# Connect to the dummy SQLite database
conn = sqlite3.connect("sales_database.db")
cursor = conn.cursor()

# Create product dimension table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT
)
""")

# Create customer dimension table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    city TEXT
)
""")

# Create date dimension table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    sale_date TEXT,
    month TEXT,
    year INTEGER
)
""")

# Create sales fact table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    sales_amount REAL,
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
)
""")

# Insert sample products
cursor.executemany("""
INSERT OR IGNORE INTO dim_product VALUES (?, ?, ?)
""", [
    (1, "Laptop", "Electronics"),
    (2, "Mobile", "Electronics"),
    (3, "Headphones", "Accessories"),
    (4, "Keyboard", "Accessories")
])

# Insert sample customers
cursor.executemany("""
INSERT OR IGNORE INTO dim_customer VALUES (?, ?, ?)
""", [
    (1, "Priya", "Chennai"),
    (2, "Arun", "Madurai"),
    (3, "Rahul", "Bangalore")
])

# Insert sample dates
cursor.executemany("""
INSERT OR IGNORE INTO dim_date VALUES (?, ?, ?, ?)
""", [
    (1, "2026-01-10", "January", 2026),
    (2, "2026-01-15", "January", 2026),
    (3, "2026-02-05", "February", 2026),
    (4, "2026-02-20", "February", 2026),
    (5, "2026-03-12", "March", 2026)
])

# Insert sample sales transactions
cursor.executemany("""
INSERT OR IGNORE INTO fact_sales VALUES (?, ?, ?, ?, ?, ?)
""", [
    (1, 1, 1, 1, 2, 100000),
    (2, 2, 2, 2, 3, 45000),
    (3, 3, 3, 3, 5, 10000),
    (4, 4, 1, 4, 4, 8000),
    (5, 1, 2, 5, 1, 50000),
    (6, 2, 3, 5, 2, 30000)
])

conn.commit()
print("Dummy star schema database created successfully!")

# MONTHLY SALES REPORT
# Join fact_sales with dim_product to get product names and categories.
# Join fact_sales with dim_date to get the monthly sales information.
# Calculate total sales amount and total quantity sold for each product.
# Group results by product name, category, month, and year.
# Sort the monthly sales report by year, month, and product name.

# GitHub Copilot: Generate a SELECT query that joins fact_sales
# with dim_product and dim_date, calculates SUM(quantity) and
# SUM(sales_amount), groups by product, category, month and year,
# and sorts by year, month and product name.

query = """
SELECT
    p.product_name,
    p.category,
    d.month,
    d.year,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales AS f
JOIN dim_product AS p
    ON f.product_id = p.product_id
JOIN dim_date AS d
    ON f.date_id = d.date_id
GROUP BY
    p.product_name,
    p.category,
    d.month,
    d.year
ORDER BY
    d.year,
    CASE d.month
        WHEN 'January' THEN 1
        WHEN 'February' THEN 2
        WHEN 'March' THEN 3
        WHEN 'April' THEN 4
        WHEN 'May' THEN 5
        WHEN 'June' THEN 6
        WHEN 'July' THEN 7
        WHEN 'August' THEN 8
        WHEN 'September' THEN 9
        WHEN 'October' THEN 10
        WHEN 'November' THEN 11
        WHEN 'December' THEN 12
    END,
    p.product_name
"""

# Verify and execute the SQL query
print("\nExecuting the verified monthly sales query...")

cursor.execute(query)
results = cursor.fetchall()

# Display the query results
print("\nMONTHLY SALES REPORT")
print("=" * 100)

columns = [description[0] for description in cursor.description]
print(" | ".join(columns))
print("-" * 100)

for row in results:
    print(" | ".join(str(value) for value in row))

print("-" * 100)
print("Total report rows:", len(results))
print("Monthly sales report generated successfully!")

# Close the database connection
conn.close()
```
