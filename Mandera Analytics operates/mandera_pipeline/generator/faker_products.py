from faker import Faker
from pymongo import MongoClient
import random

fake = Faker()

mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]

products_collection = db["products"]

products = []

for _ in range(20):
    product = {
        "product_name": fake.word().title(),
        "category": random.choice(["Electronics", "Clothing", "Food"]),
        "price": round(random.uniform(10, 500), 2),
        "stock": random.randint(1, 100)
    }

    products.append(product)

products_collection.insert_many(products)

print("✅ Fake products inserted into MongoDB")