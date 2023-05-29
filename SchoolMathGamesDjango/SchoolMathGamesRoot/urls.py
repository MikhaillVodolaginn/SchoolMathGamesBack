"""SchoolMathGamesRoot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from MathGamesApp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/gameList/", GameList.as_view()),
    path("api/v1/game/", GetGameById.as_view()),
    path("api/v1/createGame", CreateGame.as_view()),
    path("api/v1/updateGameInfo", UpdateGameInfo.as_view()),
    path("api/v1/addTeam", AddTeam.as_view()),
    path("api/v1/updateTeam", UpdateTeam.as_view()),
    path("api/v1/updateGameStatus", UpdateGameStatus.as_view()),
    path("api/v1/changeScores", ChangeScores.as_view()),
    path("api/v1/deleteGame", DeleteGame.as_view()),
    path("api/v1/deleteTeam", DeleteTeam.as_view()),
    path("api/v1/isValidToken/", CheckToken.as_view()),
    path("api/v1/auth/", include('djoser.urls')),
    re_path(r"^auth/", include('djoser.urls.authtoken'))
]
