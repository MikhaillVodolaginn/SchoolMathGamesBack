from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
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
        if name == '':
            return Response({'error': 'Название игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        gameType = request.POST.get('gameType', -1)
        if gameType == -1:
            return Response({'error': 'Тип игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        start = request.POST.get('name', -1)
        if start == -1:
            return Response({'error': 'Время начала игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        timeGame = request.POST.get('timeGame', -1)
        if timeGame == -1:
            return Response({'error': 'Продолжительность игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(GameAllInfoMock.gameAllInfo)


class GetGameById(APIView):
    @staticmethod
    def get(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        for game in GamesMock.gameList:
            if gameId == game['id']:
                return Response(GameAllInfoMock.gameAllInfo)
        return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateGameInfo(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = ''
        for game in GamesMock.gameList:
            if gameId == game['id']:
                target_game = GameAllInfoMock.gameAllInfo
                break
        if target_game == '':
            Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.POST.get('name', '')
        if not name == '':
            target_game['name'] = name
        gameType = request.POST.get('gameType', -1)
        if not gameType == -1:
            target_game['gameType'] = gameType
        start = request.POST.get('name', -1)
        if not start == -1:
            target_game['start'] = start
        timeGame = request.POST.get('timeGame', -1)
        if not timeGame == -1:
            target_game['timeGame'] = timeGame
        return Response()


class AddTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = ''
        for game in GamesMock.gameList:
            if gameId == game['id']:
                target_game = GameAllInfoMock.gameAllInfo
                break
        if target_game == '':
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.POST.get('name', '')
        if name == '':
            return Response({'error': 'Название команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response()


class UpdateTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = ''
        for game in GamesMock.gameList:
            if gameId == game['id']:
                target_game = GameAllInfoMock.gameAllInfo
                break
        if target_game == '':
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        # Костыль для постмана, если ты будешь нормально отправлять числа, такого быть не должно, но надо будет потестить
        teamId = int(request.POST.get('teamId', -1))
        if teamId == -1:
            return Response({'error': 'Идентификатор команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        target_team = ''
        for team in target_game['teams']:
            if team['id'] == teamId:
                target_team = team
                break
        if target_team == '':
            return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.POST.get('name', '')
        if name == '':
            return Response({'error': 'Новое название команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response()


class UpdateGameStatus(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = ''
        for game in GamesMock.gameList:
            if gameId == game['id']:
                target_game = GameAllInfoMock.gameAllInfo
                break
        if target_game == '':
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        game_status = request.POST.get('status', -1)
        if game_status == -1:
            return Response({'error': 'Новый статус игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game['status'] = game_status
        return Response()


class DeleteGame(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = ''
        for game in GamesMock.gameList:
            if gameId == game['id']:
                target_game = GameAllInfoMock.gameAllInfo
                break
        if target_game == '':
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response()


class DeleteTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = request.POST.get('gameId', -1)
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = ''
        for game in GamesMock.gameList:
            if gameId == game['id']:
                target_game = GameAllInfoMock.gameAllInfo
                break
        if target_game == '':
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        # Костыль для постмана, если ты будешь нормально отправлять числа, такого быть не должно, но надо будет потестить
        teamId = int(request.POST.get('teamId', -1))
        if teamId == -1:
            return Response({'error': 'Идентификатор команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        target_team = ''
        for team in target_game['teams']:
            if team['id'] == teamId:
                target_team = team
                break
        if target_team == '':
            return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response()
