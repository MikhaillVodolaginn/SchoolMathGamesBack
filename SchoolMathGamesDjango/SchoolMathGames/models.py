from django.db import models


class GamesMock:
    gameList = [
        {'id': '0', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '0', 'start': '1702371081000', 'status': '0'},
        {'id': '1', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '1', 'start': '1670835081000', 'status': '1'},
        {'id': '2', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '2', 'start': '1639299081000', 'status': '2'},
        {'id': '3', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '1', 'start': '1639299081000', 'status': '3'},
        {'id': '4', 'name': 'Первый тур чемпионата лицея №130 по Математическим Абакам', 'gameType': '0', 'start': '1607763081000', 'status': '4'},
    ]


class LoginMock:
    login: str = 'admin'
    password: str = '123456'
    accessToken: str = 'FaGfijP7Hlc49ThKRHeE'
