from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),         # Page d'accueil
    path('about/', views.about, name='about'), # Page "À propos"
    path('contact/', views.contact, name='contact'), # Page "Contact"
]
