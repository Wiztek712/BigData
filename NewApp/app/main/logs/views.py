from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game')  # Redirige vers la page d'accueil
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

"""@login_required"""

# Vue personnalisée pour rediriger vers 'about.html' après connexion
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Chemin vers le formulaire de connexion
    next_page = '/game/'  # Redirection après connexion réussiew