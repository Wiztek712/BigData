from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient  # type: ignore
from bson import ObjectId  # Pour manipuler les IDs MongoDB
from hostname import DB_URL

# Connexion à MongoDB
client = MongoClient(DB_URL)
db = client["QuickDraw"]
users_collection = db["users"]
games_collection = db["games"]  # Assurez-vous que la collection est définie
drawings_collection = db["drawings"]

@login_required
def loghome(request):
    username = request.session.get('username', None)

    # Vérifier que l'utilisateur existe bien dans MongoDB
    user = users_collection.find_one({'username': username})

    if user:
        user_id = user.get('_id')  # Récupère l'ID MongoDB

        # Nombre total de parties jouées
        total_games = games_collection.count_documents({'user_id': user_id})

        # Nombre total de dessins réalisés
        total_drawings = drawings_collection.count_documents({'user_id': user_id})

        # Nombre de dessins reconnus par l'IA
        recognized_drawings = drawings_collection.count_documents({'user_id': user_id, 'found': True})

        # Récupération du meilleur score (Best Score)
        best_game = games_collection.find_one(
            {'user_id': user_id},  # Filtrer par utilisateur
            sort=[('score', -1)]  # Trier par score décroissant
        )
        best_score = best_game['score'] if best_game else 0  # Si aucune partie, score = 0

        # Calcul du Win Rate (%)
        win_rate = (recognized_drawings / total_drawings) * 100 if total_drawings > 0 else 0
    else:
        total_games = 0
        win_rate = 0
        best_score = 0

    return render(request, 'loghome.html', {
        'username': username,
        'total_games': total_games,
        'win_rate': round(win_rate, 2),  # Arrondi à 2 décimales
        'best_score': best_score
    })

def home(request):
    return render(request, 'home.html')
