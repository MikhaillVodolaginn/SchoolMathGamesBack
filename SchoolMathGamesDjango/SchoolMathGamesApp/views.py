from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *


class GameList(APIView):
    @staticmethod
    def get(request):
        return Response(GamesMock.gameList)


class CheckToken(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        return Response({'validToken': 'true'})


class CreateGame(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        name = request.POST.get('name', '')
        gameType = request.POST.get('gameType', -1)
        start = request.POST.get('name', -1)
        timeGame = request.POST.get('timeGame', -1)
        return Response(GameAllInfoMock.gameAllInfo)


class GetGameById(APIView):
    @staticmethod
    def get(request):
        gameId = request.POST.get('gameId', -1)
        return Response(GameAllInfoMock.gameAllInfo)


class UpdateGameInfo(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        name = request.POST.get('name', '')
        gameType = request.POST.get('gameType', -1)
        start = request.POST.get('name', -1)
        timeGame = request.POST.get('timeGame', -1)
        return Response()


class AddTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        name = request.POST.get('name', '')
        gameId = request.POST.get('gameId', -1)
        return Response()


class UpdateTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        name = request.POST.get('name', '')
        gameId = request.POST.get('gameId', -1)
        teamId = request.POST.get('teamId', -1)
        return Response()


class UpdateGameStatus(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        return Response()


class DeleteGame(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        return Response()


class DeleteTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        teamId = request.POST.get('teamId', -1)
        return Response()
