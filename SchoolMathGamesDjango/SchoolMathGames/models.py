from django.db import models


class GamesMock:
    gameList = [
        {'id': '0', 'name': 'zero', 'gameType': '0', 'start': '22.02.2022', 'status': '0'},
        {'id': '1', 'name': 'one', 'gameType': '1', 'start': '21.01.2021', 'status': '1'},
        {'id': '2', 'name': 'two', 'gameType': '2', 'start': '22.02.2022', 'status': '2'},
        {'id': '3', 'name': 'three', 'gameType': '1', 'start': '23.03.2023', 'status': '3'},
        {'id': '4', 'name': 'four', 'gameType': '0', 'start': '22.02.2022', 'status': '4'},
    ]


class LoginMock:
    login: str = 'admin'
    password: str = '123456'
    accessToken: str = 'FaGfijP7Hlc49ThKRHeE'
