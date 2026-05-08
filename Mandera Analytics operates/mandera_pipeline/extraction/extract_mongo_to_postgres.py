from pymongo import MongoClient
import psycopg2

# -------------------------------
# MongoDB Connection
# -------------------------------

mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongo_client = MongoClient(mongo_uri)

mongo_db = mongo_client["mandera_db"]
mongo_collection = mongo_db["test_collection"]

# -------------------------------
# PostgreSQL Connection
# -------------------------------

postgres_conn = psycopg2.connect(
    host="localhost",
    database="mandera_db",
    user="postgres",
    password="Mandera123"
)

cursor = postgres_conn.cursor()

# -------------------------------
# Create Table
# -------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    status TEXT
)
""")

postgres_conn.commit()

# -------------------------------
# Extract Data from MongoDB
# -------------------------------

data = list(mongo_collection.find())

# -------------------------------
# Insert Data into PostgreSQL
# -------------------------------

for record in data:
    name = record.get("name", "")
    status = record.get("status", "")

    cursor.execute("""
        INSERT INTO customers (name, status)
        VALUES (%s, %s)
    """, (name, status))

postgres_conn.commit()

# -------------------------------
# Success Message
# -------------------------------

print(f"✅ Loaded {len(data)} records into PostgreSQL")

# -------------------------------
# Close Connections
# -------------------------------

cursor.close()
postgres_conn.close()
mongo_client.close()