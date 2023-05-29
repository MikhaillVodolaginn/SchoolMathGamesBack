from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *


class GameList(APIView):
    @staticmethod
    def get(request):
        games = Game.objects.all()
        gameResponse = []
        for game in games:
            teams = []
            if game.type == 0:
                for team in AbakaTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name,
                                 'scores': list(AbakaSerializer(team).data.values())}
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(-1)
                    team_resp['sumScore'] = sum(team_resp['scores'])
                    teams.append(team_resp)
            elif game.type == 1:
                for team in BonusTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name,
                                 'scores': list(BonusSerializer(team).data.values())}
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(-1)
                    team_resp['sumScore'] = sum(team_resp['scores'])
                    teams.append(team_resp)
            else:
                for team in DominoTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                                 'scores': list(DominoSerializer(team).data.values())}
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(-1)
                    for i in range(len(team_resp['scores'])):
                        if team_resp['scores'][i] == 0:
                            team_resp['sumScore'] += i
                    teams.append(team_resp)

            gameResponse.append({'id': game.game_id, 'name': game.game_name, 'status': game.status, 'type': game.type,
                                 'start': game.start, 'time': game.duration, 'teams': teams})
        return Response(gameResponse)


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
        gameType = int(request.data.get('type', -1))
        if gameType == -1:
            return Response({'error': 'Тип игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        start = int(request.data.get('start', -1))
        if start == -1:
            return Response({'error': 'Время начала игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        duration = int(request.data.get('timeGame', -1))
        if duration == -1:
            return Response({'error': 'Продолжительность игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        game = Game()
        game.game_name = name
        game.status = 0
        game.type = gameType
        game.start = start
        game.duration = duration
        game.save()

        return Response(
            {'id': game.game_id, 'name': game.game_name, 'status': game.status, 'type': game.type, 'start': game.start,
             'timeGame': game.duration, 'teams': []})


class GetGameById(APIView):
    @staticmethod
    def get(request):
        game_id = request.GET.get('id', -1)
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            game = Game.objects.get(game_id=game_id)
            teams = []
            if game.type == 0:
                for team in AbakaTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name,
                                 'scores': list(AbakaSerializer(team).data.values())}
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(-1)
                    team_resp['sumScore'] = sum(team_resp['scores'])
                    teams.append(team_resp)
            elif game.type == 1:
                for team in BonusTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name,
                                 'scores': list(BonusSerializer(team).data.values())}
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(-1)
                    team_resp['sumScore'] = sum(team_resp['scores'])
                    teams.append(team_resp)
            else:
                for team in DominoTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                                 'scores': list(DominoSerializer(team).data.values())}
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(0)
                    team_resp['scores'].pop(-1)
                    for i in range(len(team_resp['scores'])):
                        if team_resp['scores'][i] == 0:
                            team_resp['sumScore'] += i
                    teams.append(team_resp)

            return Response({'id': game.game_id, 'name': game.game_name, 'status': game.status, 'type': game.type,
                             'start': game.start, 'time': game.duration, 'teams': teams})
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateGameInfo(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

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

        teams = []
        if target_game.type == 0:
            for team in AbakaTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(AbakaSerializer(team).data.values())}
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(-1)
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        elif target_game.type == 1:
            for team in BonusTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(BonusSerializer(team).data.values())}
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(-1)
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        else:
            for team in DominoTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                             'scores': list(DominoSerializer(team).data.values())}
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(-1)
                for i in range(len(team_resp['scores'])):
                    if team_resp['scores'][i] == 0:
                        team_resp['sumScore'] += i
                teams.append(team_resp)

        return Response({'id': target_game.game_id, 'name': target_game.game_name, 'status': target_game.status,
                         'type': target_game.type, 'start': target_game.start, 'time': target_game.duration,
                         'teams': teams})


class AddTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))

        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name', '')
        if name == '':
            return Response({'error': 'Название команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        if target_game.type == 0:
            team = AbakaTeam()
        elif target_game.type == 1:
            team = BonusTeam()
        else:
            team = DominoTeam()
        team.game = target_game
        team.team_name = name
        team.save()

        if target_game.type == 0:
            return Response(AbakaSerializer(team).data)
        elif target_game.type == 1:
            return Response(BonusSerializer(team).data)
        else:
            return Response(DominoSerializer(team).data)


class UpdateTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))

        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        team_id = int(request.data.get('teamId', -1))
        if team_id == -1:
            return Response({'error': 'Идентификатор команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        if target_game.type == 0:
            try:
                team = AbakaTeam.objects.get(team_id=team_id)
            except AbakaTeam.DoesNotExist:
                return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)
        elif target_game.type == 1:
            try:
                team = BonusTeam.objects.get(team_id=team_id)
            except BonusTeam.DoesNotExist:
                return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                team = DominoTeam.objects.get(team_id=team_id)
            except DominoTeam.DoesNotExist:
                return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name', '')
        if name == '':
            return Response({'error': 'Новое название команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        team.team_name = name
        team.save()

        if target_game.type == 0:
            return Response(AbakaSerializer(team).data)
        elif target_game.type == 1:
            return Response(BonusSerializer(team).data)
        else:
            return Response(DominoSerializer(team).data)


class UpdateGameStatus(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        game_status = int(request.data.get('status', -1))
        if game_status == -1:
            return Response({'error': 'Новый статус игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game.status = game_status
        target_game.save()

        teams = []
        if target_game.type == 0:
            for team in AbakaTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(AbakaSerializer(team).data.values())}
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(-1)
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        elif target_game.type == 1:
            for team in BonusTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(BonusSerializer(team).data.values())}
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(-1)
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        else:
            for team in DominoTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                             'scores': list(DominoSerializer(team).data.values())}
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(0)
                team_resp['scores'].pop(-1)
                for i in range(len(team_resp['scores'])):
                    if team_resp['scores'][i] == 0:
                        team_resp['sumScore'] += i
                teams.append(team_resp)

        return Response({'id': target_game.game_id, 'name': target_game.game_name, 'status': target_game.status,
                         'type': target_game.type, 'start': target_game.start, 'time': target_game.duration,
                         'teams': teams})


class DeleteGame(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        target_game.delete()
        return Response()


class DeleteTeam(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        team_id = int(request.data.get('teamId', -1))

        if team_id == -1:
            return Response({'error': 'Идентификатор команды отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        if target_game.type == 0:
            try:
                target_team = AbakaTeam.objects.get(team_id=team_id)
            except AbakaTeam.DoesNotExist:
                return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)
        elif target_game.type == 1:
            try:
                target_team = BonusTeam.objects.get(team_id=team_id)
            except BonusTeam.DoesNotExist:
                return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                target_team = DominoTeam.objects.get(team_id=team_id)
            except DominoTeam.DoesNotExist:
                return Response({'error': 'Команда не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        if target_game.type == 0:
            team_resp = Response(AbakaSerializer(target_team).data)
        elif target_game.type == 1:
            team_resp = Response(BonusSerializer(target_team).data)
        else:
            team_resp = Response(DominoSerializer(target_team).data)

        target_team.delete()
        return team_resp


class ChangeScores(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        game_id = int(request.data.get('gameId', -1))
        if game_id == -1:
            return Response({'error': 'Идентификатор игры отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Игра не найдена!'}, status=status.HTTP_400_BAD_REQUEST)

        if target_game.type == 0:
            team_set = AbakaTeam.objects.filter(game=target_game)
        elif target_game.type == 1:
            team_set = BonusTeam.objects.filter(game=target_game)
        else:
            team_set = DominoTeam.objects.filter(game=target_game)

        changeScores = request.data.get('changeScores', [])

        for score in changeScores:
            team = team_set.get(team_id=score.teamId)
            team.update_field(score.exercise, score.value)
            team.save()

        return Response()

