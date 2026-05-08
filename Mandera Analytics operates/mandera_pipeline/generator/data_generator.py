from faker import Faker
from pymongo import MongoClient
import random

# Initialize Faker
fake = Faker()

# MongoDB Connection
mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]

collection = db["test_collection"]

# Create fake records
records = []

for _ in range(20):
    customer = {
        "name": fake.name(),
        "email": fake.email(),
        "country": fake.country(),
        "status": random.choice(["active", "inactive"])
    }

    records.append(customer)

# Insert into MongoDB
collection.insert_many(records)

print("✅ 20 Fake Customer Records Inserted Into MongoDB")