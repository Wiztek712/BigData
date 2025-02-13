from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ai_model.model.process import display, QuickDrawDataset
from pymongo import MongoClient  # type: ignore
from hostname import DB_URL

# Get MongoDB credentials from environment variables (for flexibility)
# MONGO_HOST = os.getenv("MONGO_HOST", "mongo_db")  # Service name from docker-compose.yml
# MONGO_PORT = os.getenv("MONGO_PORT", "27017")
# MONGO_USER = os.getenv("MONGO_USER", "myuser")
# MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mypassword")
# MONGO_DB = os.getenv("MONGO_DB", "QuickDraw")

# Connection string for MongoDB with authentication
# MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
# MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}"

# MONGO_URL = "mongodb://myuser:mypassword@localhost:27017"


client = MongoClient(DB_URL)
db = client["QuickDraw"]
print("Connected to MongoDB")
users_collection = db["users"]
drawings_collection = db["drawings"]
games_collection = db["games"]

def game(request):
    return render(request, 'game/game.html')

@login_required
def waiting_room(request):
    username = request.session.get('username', None)
    return render(request, 'game/waiting_room.html', {'username': username})

def save_game_data(request):
    username = request.session.get('username', None)
    # print('I try to do smthg')
    if request.method == 'POST':
        # print('I receive a POST')
        try:
            # print('I try one more tiome to do smthg')
            data = json.loads(request.body)
            # print('JSON loads')

            # Extract data
            user = users_collection.find_one({'username': username})
            # print("user : ", user)
            user_id = user['_id']
            # print('user_id :', user_id)

            save_drawings = data.get('saveDrawings', [])  # List of drawings
            score = data.get('score', 0)

            # Store in session
            request.session['save_drawings'] = save_drawings
            request.session['score'] = score

            # Save the game to the 'games' collection in MongoDB
            game_data = {
                "user_id": user_id,  # Store user_id as a string
                "score": score,
            }
            # print(game_data)
            game_result = games_collection.insert_one(game_data)
            game_id = game_result.inserted_id  # Get the inserted game's ID

            # Save each drawing to the 'drawings' collection
            for drawing in save_drawings:
                drawing_data = {
                    "game_id": game_id,  # Link to the game
                    "user_id": user_id,  # Store user_id as a string
                    "word": drawing.get("word", ""), # Work to guess
                    "drawing_data": drawing.get('drawing', {}),  # Drawing data
                    "time_to_draw": drawing.get('time', 0),  # Time taken
                    "found": drawing.get('recognized', False)  # Found or not
                }
                # print(drawing_data)
                drawings_collection.insert_one(drawing_data)

            # return JsonResponse({'status': 'success', 'message': 'Game data saved successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def final_results(request):
    game_data = request.session.get('save_drawings', [])
    # print(game_data)
    dataset = display(game_data)
    size = len(game_data)
    images=[]

    for i in range(size):
        drawing = dataset.__getitem__(i)
        plt.imshow(1 - drawing[0].squeeze(), cmap='gray')  # Squeeze to remove the single channel dimension
        plt.axis('off')  # Hide axis for better visualization
        plt.title(drawing[1])
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        images.append(img_str)

    results = zip(game_data, images)

    return render(request, 'game/final_results.html', {'results': results})
