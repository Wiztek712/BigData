from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

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