from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from pymongo import MongoClient # type: ignore
from .forms import SignupForm
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

MONGO_URL = "mongodb://myuser:mypassword@localhost:27017"


# client = MongoClient(MONGO_URL)
# db = client[MONGO_DB]
# print("Connected to MongoDB")

client = MongoClient(MONGO_URL)
db = client["QuickDraw"]
print("Connected to MongoDB")
users_collection = db["users"]  # Collection for users

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Insert user into MongoDB
            mongo_user = {
                "username": user.username
            }
            users_collection.insert_one(mongo_user)

            # Store username in session
            request.session['username'] = user.username

            return redirect('waiting_room')  # Redirect to waiting room
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


"""@login_required"""

# Vue personnalisée pour rediriger vers 'waiting_room.html' après connexion
class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = '/waiting-room/'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Store username in session after login
        self.request.session['username'] = self.request.user.username

        return response
