from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import GamesMock, GameAllInfoMock


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
        return Response({'gameAllInfo': GameAllInfoMock.gameAllInfo})


class GetGameById(APIView):
    @staticmethod
    def get(request):
        return Response(GamesMock.gameList[0])
