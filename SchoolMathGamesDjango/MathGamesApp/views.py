import datetime

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *


class GameList(APIView):
    @staticmethod
    def get(request):
        history = request.GET.get('history', False)
        if history == 'true':
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
                    team_resp = {'teamId': team.team_id, 'name': team.team_name}
                    scores = list(GamePointsSerializer(team).data.values())
                    sum_score = 0
                    horizontal = 0
                    vertical = [0] * 6
                    for i in range(1, 31):
                        if scores[i - 1] > 0:
                            sum_score += abaka_dict[str(i)][scores[i - 1]]
                            horizontal += 1
                            vertical[i % 6] += 1
                        if i % 6 == 0:
                            if horizontal == 6:
                                sum_score += 50
                            horizontal = 0
                    for i in range(0, 6):
                        if vertical[i] == 5:
                            sum_score += (i + 1) * 10
                    team_resp['scores'] = scores
                    team_resp['sumScore'] = sum_score
                    teams.append(team_resp)
            elif game.type == 1:
                for team in BonusTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name}
                    scores = list(GamePointsSerializer(team).data.values())
                    sum_score = 0
                    for i in range(1, 25):
                        if scores[i - 1] >= 0:
                            sum_score += bonus_dict[str(i)][scores[i - 1]]
                    team_resp['scores'] = scores
                    team_resp['sumScore'] = sum_score
                    teams.append(team_resp)
            else:
                for team in DominoTeam.objects.filter(game=game):
                    team_resp = {'teamId': team.team_id, 'name': team.team_name}
                    scores = list(GamePointsSerializerDomino(team).data.values())
                    sum_score = 0
                    for i in range(0, 28):
                        if scores[i] <= 0:
                            sum_score += domino_dict[str(i)][abs(scores[i])]
                    team_resp['scores'] = scores
                    team_resp['sumScore'] = sum_score
                    teams.append(team_resp)

            result = {'id': game.game_id, 'name': game.game_name, 'status': game.status,
                      'type': game.type, 'start': game.start, 'time': game.duration,
                      'teams': sorted(teams, key=lambda x: x['sumScore'], reverse=True)}

            if game.status == 0:
                return Response(result)

            if game.status == 1:
                result['time'] = (game.start // 1000 - int(datetime.datetime.now().timestamp())) + game.duration
            else:
                result['time'] = (game.start // 1000 - game.end_time) + game.duration

            return Response(result)
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
                team_resp = {'teamId': team.team_id, 'name': team.team_name}
                scores = list(GamePointsSerializer(team).data.values())
                sum_score = 0
                horizontal = 0
                vertical = [0] * 6
                for i in range(1, 31):
                    if scores[i - 1] > 0:
                        sum_score += abaka_dict[str(i)][scores[i - 1]]
                        horizontal += 1
                        vertical[i % 6] += 1
                    if i % 6 == 0:
                        if horizontal == 6:
                            sum_score += 50
                        horizontal = 0
                for i in range(0, 6):
                    if vertical[i] == 5:
                        sum_score += (i + 1) * 10
                team_resp['scores'] = scores
                team_resp['sumScore'] = sum_score
                teams.append(team_resp)
        elif target_game.type == 1:
            for team in BonusTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name}
                scores = list(GamePointsSerializer(team).data.values())
                sum_score = 0
                for i in range(1, 25):
                    if scores[i - 1] >= 0:
                        sum_score += bonus_dict[str(i)][scores[i - 1]]
                team_resp['scores'] = scores
                team_resp['sumScore'] = sum_score
                teams.append(team_resp)
        else:
            for team in DominoTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name}
                scores = list(GamePointsSerializerDomino(team).data.values())
                sum_score = 0
                for i in range(0, 28):
                    if scores[i] <= 0:
                        sum_score += domino_dict[str(i)][abs(scores[i])]
                team_resp['scores'] = scores
                team_resp['sumScore'] = sum_score
                teams.append(team_resp)

        return Response({'id': target_game.game_id, 'name': target_game.game_name, 'status': target_game.status,
                         'type': target_game.type, 'start': target_game.start, 'time': target_game.duration,
                         'teams': sorted(teams, key=lambda x: x['sumScore'], reverse=True)})


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

        team_resp = {'teamId': team.team_id, 'name': team.team_name}

        if target_game.type == 2:
            team_resp['scores'] = list(GamePointsSerializerDomino(team).data.values())
        else:
            team_resp['scores'] = list(GamePointsSerializer(team).data.values())

        team_resp['sumScore'] = 0

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

        team_resp = {'teamId': team.team_id, 'name': team.team_name}
        sum_score = 0

        if target_game.type == 0:
            scores = list(GamePointsSerializer(team).data.values())
            horizontal = 0
            vertical = [0] * 6
            for i in range(1, 31):
                if scores[i - 1] > 0:
                    sum_score += abaka_dict[str(i)][scores[i - 1]]
                    horizontal += 1
                    vertical[i % 6] += 1
                if i % 6 == 0:
                    if horizontal == 6:
                        sum_score += 50
                    horizontal = 0
            for i in range(0, 6):
                if vertical[i] == 5:
                    sum_score += (i + 1) * 10
            team_resp['scores'] = scores
            team_resp['sumScore'] = sum_score
        elif target_game.type == 1:
            scores = list(GamePointsSerializer(team).data.values())
            for i in range(1, 25):
                if scores[i - 1] >= 0:
                    sum_score += bonus_dict[str(i)][scores[i - 1]]
            team_resp['scores'] = scores
            team_resp['sumScore'] = sum_score
        else:
            scores = list(GamePointsSerializerDomino(team).data.values())
            for i in range(0, 28):
                if scores[i] <= 0:
                    sum_score += domino_dict[str(i)][abs(scores[i])]
            team_resp['scores'] = scores
            team_resp['sumScore'] = sum_score

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

        if game_status == 1 and target_game.status != 0:
            target_game.duration = target_game.duration + (
                    int(datetime.datetime.now().timestamp()) - target_game.end_time)

        if game_status == 2 and target_game.status == 1:
            target_game.end_time = int(datetime.datetime.now().timestamp())

        if game_status == 1 and target_game.status == 0:
            target_game.start = int(datetime.datetime.now().timestamp()) * 1000

        target_game.status = game_status
        end_time = int(request.data.get('endTime', -1))
        if not end_time == -1:
            target_game.end_time = end_time
        target_game.save()

        teams = []
        if target_game.type == 0:
            for team in AbakaTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name}
                scores = list(GamePointsSerializer(team).data.values())
                sum_score = 0
                horizontal = 0
                vertical = [0] * 6
                for i in range(1, 31):
                    if scores[i - 1] > 0:
                        sum_score += abaka_dict[str(i)][scores[i - 1]]
                        horizontal += 1
                        vertical[i % 6] += 1
                    if i % 6 == 0:
                        if horizontal == 6:
                            sum_score += 50
                        horizontal = 0
                for i in range(0, 6):
                    if vertical[i] == 5:
                        sum_score += (i + 1) * 10
                team_resp['scores'] = scores
                team_resp['sumScore'] = sum_score
                teams.append(team_resp)
        elif target_game.type == 1:
            for team in BonusTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name}
                scores = list(GamePointsSerializer(team).data.values())
                sum_score = 0
                for i in range(1, 25):
                    if scores[i - 1] >= 0:
                        sum_score += bonus_dict[str(i)][scores[i - 1]]
                team_resp['scores'] = scores
                team_resp['sumScore'] = sum_score
                teams.append(team_resp)
        else:
            for team in DominoTeam.objects.filter(game=target_game):
                team_resp = {'teamId': team.team_id, 'name': team.team_name}
                scores = list(GamePointsSerializerDomino(team).data.values())
                sum_score = 0
                for i in range(0, 28):
                    if scores[i] <= 0:
                        sum_score += domino_dict[str(i)][abs(scores[i])]
                team_resp['scores'] = scores
                team_resp['sumScore'] = sum_score
                teams.append(team_resp)

        result = {'id': target_game.game_id, 'name': target_game.game_name, 'status': target_game.status,
                  'type': target_game.type, 'start': target_game.start, 'time': target_game.duration,
                  'teams': sorted(teams, key=lambda x: x['sumScore'], reverse=True)}

        if target_game.status == 1:
            result['time'] = (target_game.start // 1000 - int(
                datetime.datetime.now().timestamp())) + target_game.duration
        else:
            result['time'] = (target_game.start // 1000 - target_game.end_time) + target_game.duration

        return Response(result)


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

        team_resp = {'teamId': target_team.team_id, 'name': target_team.team_name}
        sum_score = 0

        if target_game.type == 0:
            scores = list(GamePointsSerializer(target_team).data.values())
            horizontal = 0
            vertical = [0] * 6
            for i in range(1, 31):
                if scores[i - 1] > 0:
                    sum_score += abaka_dict[str(i)][scores[i - 1]]
                    horizontal += 1
                    vertical[i % 6] += 1
                if i % 6 == 0:
                    if horizontal == 6:
                        sum_score += 50
                    horizontal = 0
            for i in range(0, 6):
                if vertical[i] == 5:
                    sum_score += (i + 1) * 10
            team_resp['scores'] = scores
            team_resp['sumScore'] = sum_score
        elif target_game.type == 1:
            scores = list(GamePointsSerializer(target_team).data.values())
            for i in range(1, 25):
                if scores[i - 1] >= 0:
                    sum_score += bonus_dict[str(i)][scores[i - 1]]
            team_resp['scores'] = scores
            team_resp['sumScore'] = sum_score
        else:
            scores = list(GamePointsSerializerDomino(target_team).data.values())
            for i in range(0, 28):
                if scores[i] <= 0:
                    sum_score += domino_dict[str(i)][abs(scores[i])]
            team_resp['scores'] = scores
            team_resp['sumScore'] = sum_score

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
            team = team_set.get(team_id=int(score['teamId']))
            if target_game.type == 0:
                exercise = int(score['exercise']) + 1
                score['exercise'] = str(exercise)
                team.update_field(exercise, int(score['value']))
            elif target_game.type == 1:
                exercise = int(score['exercise']) + 1
                score['exercise'] = str(exercise)
                team.update_field(exercise, int(score['value']))
            else:
                exercise = int(score['exercise'])
                score['exercise'] = str(exercise)
                team.update_field(exercise, int(score['value']))
            team.save()

        return Response()


domino_dict = {'0': [0, 10],
               '1': [0, 1, 1],
               '2': [0, 2, 2],
               '3': [0, 3, 3],
               '4': [0, 4, 4],
               '5': [0, 5, 5],
               '6': [0, 6, 6],
               '7': [-1, 2, 1],
               '8': [-1, 3, 2],
               '9': [-1, 4, 3],
               '10': [-1, 5, 4],
               '11': [-1, 6, 5],
               '12': [-1, 7, 6],
               '13': [-2, 4, 2],
               '14': [-2, 5, 3],
               '15': [-2, 6, 4],
               '16': [-2, 7, 5],
               '17': [-2, 8, 6],
               '18': [-3, 6, 3],
               '19': [-3, 7, 4],
               '20': [-3, 8, 5],
               '21': [-3, 9, 6],
               '22': [-4, 8, 4],
               '23': [-4, 9, 5],
               '24': [-4, 10, 6],
               '25': [-5, 10, 5],
               '26': [-5, 11, 6],
               '27': [-6, 12, 6]}

abaka_dict = {'1': [0, 10],
              '2': [0, 20],
              '3': [0, 30],
              '4': [0, 40],
              '5': [0, 50],
              '6': [0, 60],
              '7': [0, 10],
              '8': [0, 20],
              '9': [0, 30],
              '10': [0, 40],
              '11': [0, 50],
              '12': [0, 60],
              '13': [0, 10],
              '14': [0, 20],
              '15': [0, 30],
              '16': [0, 40],
              '17': [0, 50],
              '18': [0, 60],
              '19': [0, 10],
              '20': [0, 20],
              '21': [0, 30],
              '22': [0, 40],
              '23': [0, 50],
              '24': [0, 60],
              '25': [0, 10],
              '26': [0, 20],
              '27': [0, 30],
              '28': [0, 40],
              '29': [0, 50],
              '30': [0, 60]}

bonus_dict = {'1': [0, 4, 5, 6, 6, 9, 12],
              '2': [0, 4, 5, 6, 6, 9, 12],
              '3': [0, 4, 5, 6, 6, 9, 12],
              '4': [0, 4, 5, 6, 6, 9, 12],
              '5': [0, 4, 5, 6, 6, 9, 12],
              '6': [0, 4, 5, 6, 6, 9, 12],
              '7': [0, 4, 5, 6, 6, 9, 12],
              '8': [0, 4, 5, 6, 6, 9, 12],
              '9': [0, 5, 6, 7, 8, 12, 16],
              '10': [0, 5, 6, 7, 8, 12, 16],
              '11': [0, 5, 6, 7, 8, 12, 16],
              '12': [0, 5, 6, 7, 8, 12, 16],
              '13': [0, 5, 6, 7, 8, 12, 16],
              '14': [0, 5, 6, 7, 8, 12, 16],
              '15': [0, 5, 6, 7, 8, 12, 16],
              '16': [0, 5, 6, 7, 8, 12, 16],
              '17': [0, 6, 7, 8, 10, 15, 20],
              '18': [0, 6, 7, 8, 10, 15, 20],
              '19': [0, 6, 7, 8, 10, 15, 20],
              '20': [0, 6, 7, 8, 10, 15, 20],
              '21': [0, 6, 7, 8, 10, 15, 20],
              '22': [0, 6, 7, 8, 10, 15, 20],
              '23': [0, 6, 7, 8, 10, 15, 20],
              '24': [0, 6, 7, 8, 10, 15, 20]}
