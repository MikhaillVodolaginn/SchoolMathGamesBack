from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *


class GameList(APIView):
    @staticmethod
    def get(request):
        history = bool(request.GET.get('history', False))
        if history:
            games = Game.objects.filter(status=4).order_by('-start')
        else:
            games = Game.objects.filter(~Q(status=4)).order_by('-start')

        gameResponse = [{'id': game.game_id,
                         'name': game.game_name,
                         'status': game.status,
                         'type': game.type,
                         'start': game.start,
                         'time': game.duration} for game in games]

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

        return Response({'id': game.game_id,
                         'name': game.game_name,
                         'status': game.status,
                         'type': game.type,
                         'start': game.start,
                         'timeGame': game.duration,
                         'teams': []})


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
                                 'scores': list(GamePointsSerializer(team).data.values())}
                    team_resp['sumScore'] = sum(team_resp['scores'])
                    teams.append(team_resp)
            elif game.type == 1:
                for team in BonusTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name,
                                 'scores': list(GamePointsSerializer(team).data.values())}
                    team_resp['sumScore'] = sum(team_resp['scores'])
                    teams.append(team_resp)
            else:
                for team in DominoTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                                 'scores': list(GamePointsSerializer(team).data.values())}
                    for i in range(len(team_resp['scores'])):
                        if team_resp['scores'][i] <= 0:
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
                             'scores': list(GamePointsSerializer(team).data.values())}
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        elif target_game.type == 1:
            for team in BonusTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(GamePointsSerializer(team).data.values())}
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        else:
            for team in DominoTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                             'scores': list(GamePointsSerializer(team).data.values())}
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

        team_resp = {'teamId': team.team_id, 'name': team.team_name,
                     'scores': list(GamePointsSerializer(team).data.values())}
        if target_game.type == 2:
            for i in range(len(team_resp['scores'])):
                if team_resp['scores'][i] == 0:
                    team_resp['sumScore'] += i
        else:
            team_resp['sumScore'] = sum(team_resp['scores'])

        return Response(team_resp)


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

        team_resp = {'teamId': team.team_id, 'name': team.team_name,
                     'scores': list(GamePointsSerializer(team).data.values())}
        if target_game.type == 2:
            for i in range(len(team_resp['scores'])):
                if team_resp['scores'][i] == 0:
                    team_resp['sumScore'] += i
        else:
            team_resp['sumScore'] = sum(team_resp['scores'])

        return Response(team_resp)


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
        end_time = int(request.data.get('endTime', -1))
        if not end_time == -1:
            target_game.end_time = end_time
        target_game.save()

        teams = []
        if target_game.type == 0:
            for team in AbakaTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(GamePointsSerializer(team).data.values())}
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        elif target_game.type == 1:
            for team in BonusTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name,
                             'scores': list(GamePointsSerializer(team).data.values())}
                team_resp['sumScore'] = sum(team_resp['scores'])
                teams.append(team_resp)
        else:
            for team in DominoTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0,
                             'scores': list(GamePointsSerializer(team).data.values())}
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

        team_resp = {'teamId': target_team.team_id, 'name': target_team.team_name,
                     'scores': list(GamePointsSerializer(target_team).data.values())}
        if target_game.type == 2:
            for i in range(len(team_resp['scores'])):
                if team_resp['scores'][i] == 0:
                    team_resp['sumScore'] += i
        else:
            team_resp['sumScore'] = sum(team_resp['scores'])

        target_team.delete()
        return Response(team_resp)


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
            print(score)
            team = team_set.get(team_id=int(score['teamId']))
            team.update_field(score['exercise'], score['value'])
            team.save()

        return Response()


domino_dict = {'point00': [0, 10],
               'point01': [0, 1, 1],
               'point02': [0, 2, 2],
               'point03': [0, 3, 3],
               'point04': [0, 4, 4],
               'point05': [0, 5, 5],
               'point06': [0, 6, 6],
               'point07': [-1, 2, 1],
               'point08': [-1, 3, 2],
               'point09': [-1, 4, 3],
               'point10': [-1, 5, 4],
               'point11': [-1, 6, 5],
               'point12': [-1, 7, 6],
               'point13': [-2, 4, 2],
               'point14': [-2, 5, 3],
               'point15': [-2, 6, 4],
               'point16': [-2, 7, 5],
               'point17': [-2, 8, 6],
               'point18': [-3, 6, 3],
               'point19': [-3, 7, 4],
               'point20': [-3, 8, 5],
               'point21': [-3, 9, 6],
               'point22': [-4, 8, 4],
               'point23': [-4, 9, 5],
               'point24': [-4, 10, 6],
               'point25': [-5, 10, 5],
               'point26': [-5, 11, 6],
               'point27': [-6, 12, 6]}
