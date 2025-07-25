from pymongo.mongo_client import MongoClient

# Replace it with your own password !!!!!
uri = "mongodb+srv://team:67BcCVFQdkeWDxaw@bookloommongodb.bfhbr.mongodb.net/?retryWrites=true&w=majority&appName=BookLoomMongoDB"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. Successfully connected to MongoDB!")

    # List all databases
    db_list = client.list_database_names()
    print("✅ Databases available:", db_list)

except Exception as e:
    print("❌ Connection failed:", e)

mongo_db = client["BookLoomDB"]