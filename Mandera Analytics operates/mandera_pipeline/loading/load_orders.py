import pandas as pd
import psycopg2

# Read transformed CSV
df = pd.read_csv("/Users/mac1/Mandera Analytics operates/orders_transformed.csv")

print(df.head())

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="mandera_db",
    user="postgres",
    password="Mandera123"
)

cursor = conn.cursor()

# Insert rows
for _, row in df.iterrows():

    cursor.execute("""
        INSERT INTO raw_orders (
            customer_name,
            product_name,
            quantity,
            amount,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row["customer_name"],
        row["product_name"],
        row["quantity"],
        row["amount"],
        row["status"]
    ))

conn.commit()

print("✅ Orders loaded into PostgreSQL")

cursor.close()
conn.close()