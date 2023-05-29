from django.db import models


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=255)
    status = models.IntegerField()
    type = models.IntegerField()
    start = models.IntegerField()
    duration = models.IntegerField()


class AbakaTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    point1 = models.IntegerField(default=0)
    point2 = models.IntegerField(default=0)
    point3 = models.IntegerField(default=0)
    point4 = models.IntegerField(default=0)
    point5 = models.IntegerField(default=0)
    point6 = models.IntegerField(default=0)
    point7 = models.IntegerField(default=0)
    point8 = models.IntegerField(default=0)
    point9 = models.IntegerField(default=0)
    point10 = models.IntegerField(default=0)
    point11 = models.IntegerField(default=0)
    point12 = models.IntegerField(default=0)
    point13 = models.IntegerField(default=0)
    point14 = models.IntegerField(default=0)
    point15 = models.IntegerField(default=0)
    point16 = models.IntegerField(default=0)
    point17 = models.IntegerField(default=0)
    point18 = models.IntegerField(default=0)
    point19 = models.IntegerField(default=0)
    point20 = models.IntegerField(default=0)
    point21 = models.IntegerField(default=0)
    point22 = models.IntegerField(default=0)
    point23 = models.IntegerField(default=0)
    point24 = models.IntegerField(default=0)
    point25 = models.IntegerField(default=0)
    point26 = models.IntegerField(default=0)
    point27 = models.IntegerField(default=0)
    point28 = models.IntegerField(default=0)
    point29 = models.IntegerField(default=0)
    point30 = models.IntegerField(default=0)

    def update_field(self, field, new_value):
        self.__setattr__(field, new_value)


class DominoTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    point0 = models.IntegerField(default=2)
    point1 = models.IntegerField(default=2)
    point2 = models.IntegerField(default=2)
    point3 = models.IntegerField(default=2)
    point4 = models.IntegerField(default=2)
    point5 = models.IntegerField(default=2)
    point6 = models.IntegerField(default=2)
    point7 = models.IntegerField(default=2)
    point8 = models.IntegerField(default=2)
    point9 = models.IntegerField(default=2)
    point10 = models.IntegerField(default=2)
    point11 = models.IntegerField(default=2)
    point12 = models.IntegerField(default=2)
    point13 = models.IntegerField(default=2)
    point14 = models.IntegerField(default=2)
    point15 = models.IntegerField(default=2)
    point16 = models.IntegerField(default=2)
    point17 = models.IntegerField(default=2)
    point18 = models.IntegerField(default=2)
    point19 = models.IntegerField(default=2)
    point20 = models.IntegerField(default=2)
    point21 = models.IntegerField(default=2)
    point22 = models.IntegerField(default=2)
    point23 = models.IntegerField(default=2)
    point24 = models.IntegerField(default=2)
    point25 = models.IntegerField(default=2)
    point26 = models.IntegerField(default=2)
    point27 = models.IntegerField(default=2)

    def update_field(self, field, new_value):
        self.__setattr__(field, new_value)


class BonusTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    point1 = models.IntegerField(default=0)
    point2 = models.IntegerField(default=0)
    point3 = models.IntegerField(default=0)
    point4 = models.IntegerField(default=0)
    point5 = models.IntegerField(default=0)
    point6 = models.IntegerField(default=0)
    point7 = models.IntegerField(default=0)
    point8 = models.IntegerField(default=0)
    point9 = models.IntegerField(default=0)
    point10 = models.IntegerField(default=0)
    point11 = models.IntegerField(default=0)
    point12 = models.IntegerField(default=0)
    point13 = models.IntegerField(default=0)
    point14 = models.IntegerField(default=0)
    point15 = models.IntegerField(default=0)
    point16 = models.IntegerField(default=0)
    point17 = models.IntegerField(default=0)
    point18 = models.IntegerField(default=0)
    point19 = models.IntegerField(default=0)
    point20 = models.IntegerField(default=0)
    point21 = models.IntegerField(default=0)
    point22 = models.IntegerField(default=0)
    point23 = models.IntegerField(default=0)
    point24 = models.IntegerField(default=0)

    def update_field(self, field, new_value):
        self.__setattr__(field, new_value)
