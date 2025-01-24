from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'myapp/about.html')

def contact(request):
    return render(request, 'myapp/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('about')  # Redirige vers la page d'accueil
    else:
        form = SignupForm()
    return render(request, 'myapp/signup.html', {'form': form})

"""@login_required"""



# Vue personnalisée pour rediriger vers 'about.html' après connexion
class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'  # Chemin vers le formulaire de connexion
    next_page = '/about/'  # Redirection après connexion réussie

# API
drawing_data = {
    "_id": "0",
    "word": "unknown",
    "drawing": [],
    "user": "default_user",
    "recognitionTime": 0,
    "recognized": False,
    "timestamp": ""
}

@csrf_exempt
def update_drawing(request):
    """
    API endpoint to update and fetch the drawing data in real-time.
    """
    global drawing_data
    if request.method == "POST":
        try:
            # Parse the JSON data sent from the frontend
            received_data = json.loads(request.body)
            drawing_data.update(received_data)
            return JsonResponse({"status": "success", "message": "Drawing updated!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    elif request.method == "GET":
        return JsonResponse(drawing_data)

    return JsonResponse({"status": "error", "message": "Unsupported method!"}, status=405)
