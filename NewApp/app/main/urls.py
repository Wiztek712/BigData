"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ai_model.views import download_model, predict
from game.views import game, waiting_room, final_results, save_game_data
from logs.views import CustomLoginView, signup
from logs.views import logout_view, logout_page
from home.views import home, loghome
from leaderboard.views import leaderboard

urlpatterns = [
    path('loghome/', loghome, name='log_home'), # Log welcoming page
    path('', home, name='home'), # Welcoming page
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('logout_page/', logout_page, name='logout_page'),
    path('admin/', admin.site.urls),
    path('game/', game, name='game'), # Used for playing
    path('waiting-room/', waiting_room, name='waiting_room'), # Before the game
    path('final-results/', final_results, name='final_results'), # End of the game
    path('save_game_data/', save_game_data, name='save_game_data'), # Save data to database
    path('leaderboard/', leaderboard, name='leaderboard'), # Display the leaderboard
    path('model/', download_model, name='ai_model'), # Used for updating the ai_model
    path('predict/', predict, name='predict'), # Used for sending the drawing
    path('signup/', signup, name='signup'), # Used for logging
    path('login/', CustomLoginView.as_view(), name='login'), # Used for Signing
]
