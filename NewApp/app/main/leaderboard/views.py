from django.shortcuts import render
from pymongo import MongoClient  # type: ignore
import os

# Get MongoDB credentials from environment variables (for flexibility)
MONGO_HOST = os.getenv("MONGO_HOST", "mongo_db")  # Service name from docker-compose.yml
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USER = os.getenv("MONGO_USER", "myuser")  
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mypassword")
MONGO_DB = os.getenv("MONGO_DB", "QuickDraw")

# Connection string for MongoDB with authentication
# MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
# MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}"

MONGO_URL = "mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017"


# client = MongoClient(MONGO_URL)
# db = client[MONGO_DB]
# print("Connected to MongoDB")

client = MongoClient(MONGO_URL)
db = client["QuickDraw"]
print("Connected to MongoDB")

users_collection = db["users"]
games_collection = db["games"]

from bson import ObjectId

def leaderboard(request):
    username = request.session.get('username', None)
    user = users_collection.find_one({'username': username})
    # print("user :", user)

    user_id = user['_id']
    # print("user_id :", user_id)

    user['user_id_str'] = user['_id']

    # Convert users' ObjectId to a new key 'user_id_str' to avoid `_id` issues in the template
    users = list(users_collection.find())
    for user in users:
        user['user_id'] = user['_id']  # Rename `_id` to `user_id_str`
    # print('users : ',users)

    # Convert game user_id to string
    player_data = list(games_collection.find({"user_id": user_id}))
    for game in player_data:
        game['game_id'] = game['_id']
    # print('player_data : ', player_data)    

    global_data = list(games_collection.find().sort("score", -1))  # Get top 10 only
    for game in global_data:
        game['game_id'] = game['_id']
    # print("global_data :", global_data)

    return render(request, 'leaderboard.html', {
        'username': username,
        'player_data': player_data,
        'global_data': global_data,
        'users_collection': users
    })
