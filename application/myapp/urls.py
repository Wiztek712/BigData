from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),         # Page d'accueil
    path('about/', views.about, name='about'), # Page "À propos"
    path('contact/', views.contact, name='contact'), # Page "Contact"
    path('signup/', views.signup, name='signup'), # Page "Signup"
    path('login/', CustomLoginView.as_view(), name='login'),
]
