from pymongo import MongoClient
from minio import Minio
import json

# --------------------------------
# MongoDB Connection
# --------------------------------

mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongo_client = MongoClient(mongo_uri)

mongo_db = mongo_client["mandera_db"]
mongo_collection = mongo_db["test_collection"]

# --------------------------------
# Extract Data
# --------------------------------

data = list(mongo_collection.find())

# Convert ObjectId to string
for record in data:
    record["_id"] = str(record["_id"])

# Save locally as JSON
with open("customers.json", "w") as file:
    json.dump(data, file, indent=4)

print("✅ JSON file created")

# --------------------------------
# MinIO Connection
# --------------------------------

minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "mandera-data"

# Create bucket if it doesn't exist
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
    print(f"✅ Bucket '{bucket_name}' created")

# Upload file
minio_client.fput_object(
    bucket_name,
    "customers.json",
    "customers.json"
)

print("✅ File uploaded to MinIO")