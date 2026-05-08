from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]
collection = db["customers"]

# Fetch data
data = list(collection.find())

# Convert to DataFrame
df = pd.DataFrame(data)

# Remove MongoDB ID
if "_id" in df.columns:
    df.drop(columns=["_id"], inplace=True)

# Clean customer names
df["name"] = df["name"].str.title()

# Remove duplicate customers
df.drop_duplicates(inplace=True)

# Save transformed data
df.to_csv("customers_transformed.csv", index=False)

print("✅ Customers transformed successfully")
print(df.head())