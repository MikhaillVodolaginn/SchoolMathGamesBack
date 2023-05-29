import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers
from django.core.serializers import serialize
from .models import *


class GameList(APIView):
    @staticmethod
    def get(request):
        games = Game.objects.all()
        gameResponse = []
        for game in games:
            gameResponse.append({'id': game.game_id, 'name': game.game_name, 'status': game.status, 'type': game.type,
                                 'start': game.start, 'time': game.duration})
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
            return Response({'id': game.game_id, 'name': game.game_name, 'status': game.status, 'type': game.type,
                             'start': game.start, 'timeGame': game.duration, 'teams': []})
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
        return Response({'id': target_game.game_id, 'name': target_game.game_name, 'status': target_game.status,
                         'type': target_game.type, 'start': target_game.start, 'time': target_game.duration})


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

        team_resp = get_team_with_scores(target_game, team)

        return Response(team_resp)

        # team_response = {'teamId': team.team_id, 'gameId': team.game.game_id, 'name': team.team_name}
        # scores = []
        # team_response['scores'] = scores
        #
        # if target_game.type == 2:
        #     scores.append(team.point0)
        #
        # scores.extend([team.point1, team.point2, team.point3, team.point4,
        #                team.point5, team.point6, team.point7, team.point8,
        #                team.point9, team.point10, team.point11, team.point12,
        #                team.point13, team.point14, team.point15, team.point16,
        #                team.point17, team.point18, team.point19, team.point20,
        #                team.point21, team.point22, team.point23, team.point24]
        #               )
        #
        # if target_game.type == 1:
        #     return Response(team_response)
        #
        # scores.extend([team.point25, team.point26, team.point27])
        #
        # if target_game.type == 2:
        #     return Response(team_response)
        #
        # scores.extend([team.point28, team.point29, team.point30])
        #
        # return Response(team_response)


def get_team_with_scores(game, team):
    team_with_scores = {'teamId': team.team_id, 'name': team.team_name, 'sumScore': 0}
    scores = []
    team_with_scores['scores'] = scores

    if game.type == 2:
        scores.append(team.point0)

    scores.extend([team.point1, team.point2, team.point3, team.point4,
                   team.point5, team.point6, team.point7, team.point8,
                   team.point9, team.point10, team.point11, team.point12,
                   team.point13, team.point14, team.point15, team.point16,
                   team.point17, team.point18, team.point19, team.point20,
                   team.point21, team.point22, team.point23, team.point24]
                  )

    if game.type == 1:
        return team_with_scores

    scores.extend([team.point25, team.point26, team.point27])

    if game.type == 2:
        return team_with_scores

    scores.extend([team.point28, team.point29, team.point30])

    return team_with_scores


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

        return Response(get_team_with_scores(target_game, team))

        # teamResponse = {'teamId': team.team_id, 'gameId': team.game.game_id, 'name': team.team_name}
        # if target_game.type == 2:
        #     teamResponse['point0'] = team.point0
        #
        # teamResponse |= {'points1': team.point1, 'points2': team.point2, 'points3': team.point3, 'points4': team.point4,
        #                  'points5': team.point5, 'points6': team.point6, 'points7': team.point7, 'points8': team.point8,
        #                  'points9': team.point9, 'points10': team.point10, 'points11': team.point11,
        #                  'points12': team.point12,
        #                  'points13': team.point13, 'points14': team.point14, 'points15': team.point15,
        #                  'points16': team.point16,
        #                  'points17': team.point17, 'points18': team.point18, 'points19': team.point19,
        #                  'points20': team.point20,
        #                  'points21': team.point21, 'points22': team.point22, 'points23': team.point23,
        #                  'points24': team.point24}
        # if target_game.type == 1:
        #     return Response(teamResponse)
        #
        # teamResponse |= {'points25': team.point25, 'points26': team.point26, 'points27': team.point27}
        # if target_game.type == 2:
        #     return Response(teamResponse)
        #
        # teamResponse |= {'points28': team.point28, 'points29': team.point29, 'points30': team.point30}
        # return Response(teamResponse)


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
        return Response({'id': target_game.game_id, 'name': target_game.game_name, 'status': target_game.status,
                         'type': target_game.type, 'start': target_game.start, 'time': target_game.duration,
                         'teams': []})


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

        team_resp = get_team_with_scores(target_game, target_team)

        target_team.delete()
        return Response(team_resp)
