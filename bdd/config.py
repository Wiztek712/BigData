from pymongo import MongoClient # type: ignore

# Connexion à MongoDB
MONGO_URL = "localhost:27017"

try:
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

    # # Exemple d'ajout de données
    # user_id = db["users"].insert_one({"username": "player1"}).inserted_id
    # print(f"Utilisateur inséré avec ID : {user_id}")

    # game_id = db["games"].insert_one({"user_id": user_id, "score": 0}).inserted_id
    # print(f"Game insérée avec ID : {game_id}")

    # drawing_id = db["drawings"].insert_one({
    #     "user_id": user_id,
    #     "game_id": game_id,
    #     "time": 1234567890,  # Remplace par un timestamp réel
    #     "found": False
    #     "drawing":[[[]]]
    # }).inserted_id
    # print(f"Dessin inséré avec ID : {drawing_id}")

except Exception as e:
    print("Erreur lors de la connexion ou de l'insertion :", e)

finally:
    client.close()
