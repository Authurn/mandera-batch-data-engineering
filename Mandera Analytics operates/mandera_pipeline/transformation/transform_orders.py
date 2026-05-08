from pymongo import MongoClient
import pandas as pd

mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client["mandera_db"]
collection = db["orders"]

data = list(collection.find())

df = pd.DataFrame(data)

if "_id" in df.columns:
    df.drop(columns=["_id"], inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill missing values
df.fillna("Unknown", inplace=True)

df.to_csv("orders_transformed.csv", index=False)

print("✅ Orders transformed successfully")
print(df.head())