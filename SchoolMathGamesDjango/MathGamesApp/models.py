from django.db import models


class GamesMock:
    gameList = [
        {'id': '0', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '0', 'start': '1702371081000', 'status': '0'},
        {'id': '1', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '1', 'start': '1670835081000', 'status': '1'},
        {'id': '2', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '2', 'start': '1639299081000', 'status': '2'},
        {'id': '3', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '1', 'start': '1639299081000', 'status': '3'},
        {'id': '4', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '0', 'start': '1607763081000', 'status': '4'},
    ]


class GameAllInfoMock:
    gameAllInfo = {
        'id': 0,
        'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам',
        'gameType': 0,
        'start': 1702371081000,
        'status': 0,
        'timeGame': 12600,
        'teams': [
            {'id': 0, 'name': 'Барабашки', 'sumScore': 30, 'scores': ['+1', '+2', '+3', '+4', '+5', '+6']},
            {'id': 1, 'name': 'Тугрики', 'sumScore': 30, 'scores': ['+1', '+2', '+3', '+4', '+5', '+6']},
            {'id': 2, 'name': 'Абвгдеёжзик', 'sumScore': 30, 'scores': ['+1', '+2', '+3', '+4', '+5', '+6']},
            {'id': 3, 'name': 'Джаваскриптизёры', 'sumScore': 30, 'scores': ['+1', '+2', '+3', '+4', '+5', '+6']}
        ]
    }

    games = [
        gameAllInfo,
    ]


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=255)
    status = models.IntegerField()
    type = models.IntegerField()
    start = models.IntegerField()
    duration = models.IntegerField()


class AbakaTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    point1 = models.IntegerField()
    point2 = models.IntegerField()
    point3 = models.IntegerField()
    point4 = models.IntegerField()
    point5 = models.IntegerField()
    point6 = models.IntegerField()
    point7 = models.IntegerField()
    point8 = models.IntegerField()
    point9 = models.IntegerField()
    point10 = models.IntegerField()
    point11 = models.IntegerField()
    point12 = models.IntegerField()
    point13 = models.IntegerField()
    point14 = models.IntegerField()
    point15 = models.IntegerField()
    point16 = models.IntegerField()
    point17 = models.IntegerField()
    point18 = models.IntegerField()
    point19 = models.IntegerField()
    point20 = models.IntegerField()
    point21 = models.IntegerField()
    point22 = models.IntegerField()
    point23 = models.IntegerField()
    point24 = models.IntegerField()
    point25 = models.IntegerField()
    point26 = models.IntegerField()
    point27 = models.IntegerField()
    point28 = models.IntegerField()
    point29 = models.IntegerField()
    point30 = models.IntegerField()


class DominoTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    point0 = models.IntegerField()
    point1 = models.IntegerField()
    point2 = models.IntegerField()
    point3 = models.IntegerField()
    point4 = models.IntegerField()
    point5 = models.IntegerField()
    point6 = models.IntegerField()
    point7 = models.IntegerField()
    point8 = models.IntegerField()
    point9 = models.IntegerField()
    point10 = models.IntegerField()
    point11 = models.IntegerField()
    point12 = models.IntegerField()
    point13 = models.IntegerField()
    point14 = models.IntegerField()
    point15 = models.IntegerField()
    point16 = models.IntegerField()
    point17 = models.IntegerField()
    point18 = models.IntegerField()
    point19 = models.IntegerField()
    point20 = models.IntegerField()
    point21 = models.IntegerField()
    point22 = models.IntegerField()
    point23 = models.IntegerField()
    point24 = models.IntegerField()
    point25 = models.IntegerField()
    point26 = models.IntegerField()
    point27 = models.IntegerField()


class BonusTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    point1 = models.IntegerField()
    point2 = models.IntegerField()
    point3 = models.IntegerField()
    point4 = models.IntegerField()
    point5 = models.IntegerField()
    point6 = models.IntegerField()
    point7 = models.IntegerField()
    point8 = models.IntegerField()
    point9 = models.IntegerField()
    point10 = models.IntegerField()
    point11 = models.IntegerField()
    point12 = models.IntegerField()
    point13 = models.IntegerField()
    point14 = models.IntegerField()
    point15 = models.IntegerField()
    point16 = models.IntegerField()
    point17 = models.IntegerField()
    point18 = models.IntegerField()
    point19 = models.IntegerField()
    point20 = models.IntegerField()
    point21 = models.IntegerField()
    point22 = models.IntegerField()
    point23 = models.IntegerField()
    point24 = models.IntegerField()
