import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("/Users/mac1/Mandera Analytics operates/customers_transformed.csv")

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
        INSERT INTO raw_customers (
            customer_id,
            name,
            email,
            country
        )
        VALUES (%s, %s, %s, %s)
    """, (
        str(row["customer_id"]),
        row["name"],
        row["email"],
        row["country"]
    ))

conn.commit()

print("✅ Customers loaded into PostgreSQL")

cursor.close()
conn.close()