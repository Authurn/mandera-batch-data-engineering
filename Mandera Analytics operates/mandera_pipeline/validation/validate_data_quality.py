from pymongo import MongoClient

# MongoDB Connection
mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]
collection = db["test_collection"]

# Fetch data
data = list(collection.find())

print(f"✅ Total Records Found: {len(data)}")

# Validate records
invalid_records = []

for record in data:

    if "name" not in record or not record["name"]:
        invalid_records.append(record)

    if "status" not in record or not record["status"]:
        invalid_records.append(record)

# Results
if len(invalid_records) == 0:
    print("✅ Data Quality Check Passed")
else:
    print(f"❌ Found {len(invalid_records)} invalid records")