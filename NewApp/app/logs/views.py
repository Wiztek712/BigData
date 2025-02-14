from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from pymongo import MongoClient # type: ignore
from .forms import SignupForm
from django.contrib.auth import logout

# MONGO_URL = "mongodb://myuser:mypassword@localhost:27017"
from hostname import DB_URL

client = MongoClient(DB_URL)
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

            return redirect('loghome')  # Redirect to waiting room
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})




def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    request.session.flush()  # Supprime toutes les données de session
    return redirect('logout_page')  # Redirige vers la page de confirmation

def logout_page(request):
    return render(request, 'logout.html')  # Affiche la page de confirmation


"""@login_required"""

# Vue personnalisée pour rediriger vers 'waiting_room.html' après connexion
class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = '/log_home/'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Store username in session after login
        self.request.session['username'] = self.request.user.username

        return response
