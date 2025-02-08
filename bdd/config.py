from pymongo import MongoClient

# Connect to MongoDB (make sure MongoDB server is running)
client = MongoClient("mongodb://localhost:27017/")

# Create a database named "mydatabase"
db = client["QuickDraw"]

# Create collections (tables in SQL terms)
users_collection = db["users"]
drawings_collection = db["drawings"]
scores_collection = db["scores"]

# Insert sample data into each collection
users_collection.insert_many([
    {"username": "Alice"},
    {"usernname": "Bob"}
])

# drawings_collection.insert_many([
    
# ])

# scores_collection.insert_many([
#     {"name": "Laptop", "category": "Electronics", "price": 1200},
#     {"name": "Phone", "category": "Electronics", "price": 800}
# ])

print("Database and collections created successfully!")

# Verify by listing databases and collections
print("Databases:", client.list_database_names())
print("Collections in mydatabase:", db.list_collection_names())

# Close the connection
client.close()
