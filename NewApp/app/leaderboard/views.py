from django.shortcuts import render
from pymongo import MongoClient  # type: ignore
from bson import ObjectId
from hostname import DB_URL

# Connexion à MongoDB
client = MongoClient(DB_URL)
db = client["QuickDraw"]
print("Connected to MongoDB")

users_collection = db["users"]
games_collection = db["games"]

def leaderboard(request):
    username = request.session.get('username', None)

    # Vérifier si l'utilisateur existe
    user = users_collection.find_one({'username': username})
    user_id = user['_id'] if user else None

    # Regrouper les scores par utilisateur (meilleur score)
    pipeline = [
        {"$group": {
            "_id": "$user_id",
            "best_score": {"$max": "$score"}  # Prend le meilleur score de chaque joueur
        }},
        {"$sort": {"best_score": -1}},  # Trie par meilleur score décroissant
    ]

    global_data = list(games_collection.aggregate(pipeline))

    # Associer les usernames aux user_id
    user_ids = [entry["_id"] for entry in global_data]
    users = {str(u["_id"]): u["username"] for u in users_collection.find({"_id": {"$in": user_ids}})}

    # Ajouter les noms d'utilisateurs au leaderboard et transformer `_id` en `id`
    for i, entry in enumerate(global_data, start=1):
        entry["username"] = users.get(str(entry["_id"]), "Unknown Player")
        entry["id"] = str(entry["_id"])  # Renommer `_id` en `id`
        entry["rank"] = i  # Ajouter le classement global
        del entry["_id"]  # Supprimer `_id` pour éviter le bug Django

    # Créer un dictionnaire pour retrouver le classement par user_id
    ranking_dict = {entry["id"]: entry["rank"] for entry in global_data}

    # Récupération des scores personnels du joueur connecté
    player_data = []
    if user_id:
        player_games = games_collection.find({"user_id": user_id}).sort("score", -1).limit(10)
        player_data = list(player_games)
        for game in player_data:
            game["id"] = str(game["_id"])  # Renommer `_id` en `id`
            game["rank"] = ranking_dict.get(str(game["user_id"]), "N/A")  # Récupérer le classement global
            del game["_id"]

    return render(request, 'leaderboard.html', {
        'username': username,
        'global_data': global_data,
        'player_data': player_data
    })
