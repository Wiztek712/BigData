from pymongo import MongoClient # type: ignore
# from pymongo.server_api import ServerApi
import os

# Get MongoDB credentials from environment variables (for flexibility)
# MONGO_HOST = os.getenv("MONGO_HOST", "mongo_db")  # Service name from docker-compose.yml
# MONGO_PORT = os.getenv("MONGO_PORT", "27017")
# MONGO_USER = os.getenv("MONGO_USER", "myuser")  
# MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mypassword")
# MONGO_DB = os.getenv("MONGO_DB", "QuickDraw")

# Connection string for MongoDB with authentication
# MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
# MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}"

# MONGO_URL = "mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017"
MONGO_URL = "mongodb+srv://rabanquentin:Yl9svhJSF3F0Fodp@mongo.yrj08.mongodb.net/?retryWrites=true&w=majority&appName=mongo"

try:
    # client = MongoClient(MONGO_URL)
    # db = client[MONGO_DB]
    # print("Connected to MongoDB")

    client = MongoClient(MONGO_URL)
    db = client["QuickDraw"]
    print("Connected to MongoDB")

    # Création des collections avec index
    db["users"].create_index([("username", 1)], unique=True)  # ID unique pour users
    print("Collection 'users' créée avec index unique sur _id")

    db["games"].create_index([("user_id", 1)])  # Index pour recherche rapide par utilisateur
    db["games"].create_index([("score", 1)])  # Index pour recherche rapide par score (classement)
    print("Collection 'games' créée avec index unique sur _id et index sur user_id")

    db["drawings"].create_index([("user_id", 1)])  # Index pour liaison avec users
    db["drawings"].create_index([("game_id", 1)])  # Index pour liaison avec games
    db["drawings"].create_index([("found", 1)])  # Index sur le champ boolean found
    print("Collection 'drawings' créée avec index unique sur _id, user_id, game_id et found")

except Exception as e:
    print("Erreur lors de la connexion ou de l'insertion :", e)

finally:
    client.close()
