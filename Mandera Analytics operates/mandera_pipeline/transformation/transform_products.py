from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]
collection = db["products"]

# Fetch data
data = list(collection.find())

# Convert to DataFrame
df = pd.DataFrame(data)

# Check if collection is empty
if df.empty:
    print("❌ No product data found in MongoDB")
    exit()

# Remove MongoDB _id
if "_id" in df.columns:
    df.drop(columns=["_id"], inplace=True)

# Show available columns
print("Available Columns:")
print(df.columns)

# Clean product column if it exists
if "product_name" in df.columns:
    df["product_name"] = df["product_name"].astype(str).str.title()

# Remove duplicates
df.drop_duplicates(inplace=True)

# Save transformed data
df.to_csv("products_transformed.csv", index=False)

print("✅ Products transformed successfully")
print(df.head())