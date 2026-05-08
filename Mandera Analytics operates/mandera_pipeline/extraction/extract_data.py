from pymongo import MongoClient

def extract():
    try:
        # Direct MongoDB URI
        mongo_uri = "mongodb+srv://mandera_user:Mandera123@cluster0.perrgjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        print("DEBUG URI:", mongo_uri)

        # Connect to MongoDB
        client = MongoClient(mongo_uri)

        # Database
        db = client["mandera_db"]

        # Collection
        collection = db["test_collection"]

        # Extract data
        data = list(collection.find())

        print(f"Extracted {len(data)} records from MongoDB")

        return data

    except Exception as e:
        print(f"Error during extraction: {e}")
        return []


if __name__ == "__main__":
    extract()