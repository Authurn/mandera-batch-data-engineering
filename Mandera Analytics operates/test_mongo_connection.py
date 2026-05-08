from pymongo import MongoClient
import certifi

uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

try:
    print(client.list_database_names())
    print("✅ MongoDB connection SUCCESS")
except Exception as e:
    print("❌ Connection FAILED:", e)