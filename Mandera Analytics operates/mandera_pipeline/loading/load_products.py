import pandas as pd
import psycopg2

# Read transformed CSV
df = pd.read_csv("/Users/mac1/Mandera Analytics operates/products_transformed.csv")

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
        INSERT INTO raw_products (
            product_name,
            category,
            price,
            stock
        )
        VALUES (%s, %s, %s, %s)
    """, (
        row["product_name"],
        row["category"],
        row["price"],
        row["stock"]
    ))

conn.commit()

print("✅ Products loaded into PostgreSQL")

cursor.close()
conn.close()