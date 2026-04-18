#!/usr/bin/env python3
"""
Quick setup script to create raw tables and insert sample data for testing.
"""

import psycopg2
from faker import Faker
from datetime import datetime, timezone
import uuid

# Database connection
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5435,
    "database": "mandera_warehouse",
    "user": "pipeline",
    "password": "pipeline_secret"
}

def create_tables():
    """Create the raw schema and customers_raw table."""
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()

    # Create raw schema if it doesn't exist
    cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    # Create customers_raw table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.customers_raw (
            customer_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            city VARCHAR(100),
            batch_id VARCHAR(50),
            created_at TIMESTAMP
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✓ Created raw.customers_raw table")

def insert_sample_data():
    """Insert some sample customer data."""
    fake = Faker()
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()

    batch_id = str(uuid.uuid4())[:8]

    customers = []
    for i in range(10):
        customer = (
            f"CUST{i:03d}",
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.city(),
            batch_id,
            datetime.now(timezone.utc)
        )
        customers.append(customer)

    cursor.executemany("""
        INSERT INTO raw.customers_raw (customer_id, name, email, phone, city, batch_id, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING;
    """, customers)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✓ Inserted {len(customers)} sample customers")

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("✓ Setup complete!")