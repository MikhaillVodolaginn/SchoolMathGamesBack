from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *


class GameList(APIView):
    @staticmethod
    def get(request):
        return Response(Game.objects.all())


class CheckToken(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        return Response({'validToken': 'true'})


class CreateGame(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        name = request.data.get('name', '')
        if name == '':
            return Response({'error': 'Название игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        gameType = int(request.data.get('gameType', -1))
        if gameType == -1:
            return Response({'error': 'Тип игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        start = int(request.data.get('start', -1))
        if start == -1:
            return Response({'error': 'Время начала игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        duration = int(request.data.get('timeGame', -1))
        if duration == -1:
            return Response({'error': 'Продолжительность игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        game = Game()
        game.name = name
        game.status = 0
        game.type = gameType
        game.start = start
        game.duration = duration
        game.save()

        return Response(game)


class GetGameById(APIView):
    @staticmethod
    def get(request):
        game_id = request.GET.get('id', -1)
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            game = Game.objects.get(game_id=game_id)
            return Response(game)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateGameInfo(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = None
        try:
            target_game = Game.objects.filter(game_id=game_id)[0]
        except Game.DoesNotExist:
            Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name', '')
        if not name == '':
            target_game.game_name = name

        start = int(request.data.get('start', -1))
        if not start == -1:
            target_game.start = start

        timeGame = int(request.data.get('timeGame', -1))
        if not timeGame == -1:
            target_game.duration = timeGame

        target_game.save()
        return Response(target_game)


class AddTeam(APIView):
    permission_classes = [IsAuthenticated]
    id = 5

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))

        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = None
        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name', '')
        if name == '':
            return Response({'error': 'Название команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        team = {'id': AddTeam.id, 'name': name, 'sumScore': 30, 'scores': ['+1', '+2', '+3', '+4', '+5', '+6']}
        AddTeam.id += 1
        target_game['teams'].append(team)

        return Response(team)


class UpdateTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = None
        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        # Костыль для постмана, если ты будешь нормально отправлять числа, такого быть не должно, но надо будет потестить
        teamId = int(request.data.get('teamId', -1))
        if teamId == -1:
            return Response({'error': 'Идентификатор команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        target_team = None
        for team in target_game['teams']:
            if int(team['id']) == teamId:
                target_team = team
                break

        if target_team is None:
            return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name', '')
        if name == '':
            return Response({'error': 'Новое название команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_team['name'] = name
        return Response(target_team)


class UpdateGameStatus(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = None
        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        game_status = int(request.data.get('status', -1))
        if game_status == -1:
            return Response({'error': 'Новый статус игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game.status = game_status
        target_game.save()
        return Response(target_game)


class DeleteGame(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = None
        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game.delete()
        return Response()


class DeleteTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gameId = int(request.data.get('gameId', -1))
        if gameId == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game = None
        for game in GamesMock.gameList:
            if gameId == int(game['id']):
                target_game = GameAllInfoMock.games[0]
                break

        if target_game is None:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        # Костыль для постмана, если ты будешь нормально отправлять числа, такого быть не должно, но надо будет потестить
        teamId = int(request.data.get('teamId', -1))
        if teamId == -1:
            return Response({'error': 'Идентификатор команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        target_team = None
        for i, team in enumerate(target_game['teams']):
            if int(team['id']) == teamId:
                target_game['teams'].pop(i)
                target_team = team
                break

        if target_team is None:
            return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(target_team)
