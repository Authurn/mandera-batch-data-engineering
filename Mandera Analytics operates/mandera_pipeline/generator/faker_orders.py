from faker import Faker
from pymongo import MongoClient
import random

fake = Faker()

mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]

orders_collection = db["orders"]

orders = []

for _ in range(20):
    order = {
        "customer_name": fake.name(),
        "product_name": fake.word().title(),
        "quantity": random.randint(1, 10),
        "amount": round(random.uniform(20, 1000), 2),
        "status": random.choice(["Pending", "Completed", "Cancelled"])
    }

    orders.append(order)

orders_collection.insert_many(orders)

print("✅ Fake orders inserted into MongoDB")