from pymongo import MongoClient

mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]
collection = db["test_collection"]

# Clear old test data
collection.delete_many({})

# Insert clean records
records = [
    {"name": "Authur", "status": "active"},
    {"name": "John", "status": "inactive"}
]

collection.insert_many(records)

print("✅ Clean records inserted")