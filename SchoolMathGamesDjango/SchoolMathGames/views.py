from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import GamesMock, LoginMock


class GameList(APIView):
    @staticmethod
    def get(request):
        return Response(GamesMock.gameList)


class Login(APIView):
    @staticmethod
    def get(request):
        login = request.query_params.get('login', '')
        password = request.query_params.get('password', '')
        if login == LoginMock.login and password == LoginMock.password:
            return Response({'accessToken': LoginMock.accessToken})
        else:
            return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)


class AccessToken(APIView):
    @staticmethod
    def get(request):
        if request.GET.get('accessToken', '') == LoginMock.accessToken:
            return Response({'validToken': True})
        else:
            return Response({'validToken': False})
