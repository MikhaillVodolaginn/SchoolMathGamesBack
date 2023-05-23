"""SchoolMathGamesDjango URL Configuration

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
from SchoolMathGames.views import GameList, SecretGameList, CheckToken, GetGameById, CreateGame

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/games/", GameList.as_view()),
    path("api/v1/secretGames/", SecretGameList.as_view()),
    path("api/v1/isValidToken/", CheckToken.as_view()),
    path("api/v1/game", GetGameById.as_view()),
    path("api/v1/create-game", CreateGame.as_view()),
    path("api/v1/auth/", include('djoser.urls')),
    re_path(r"^auth/", include('djoser.urls.authtoken'))
]
