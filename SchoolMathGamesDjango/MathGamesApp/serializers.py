from rest_framework import serializers
from .models import *


class GamePointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbakaTeam
        exclude = ['team_id', 'game', 'team_name']


class GamePointsSerializerDomino(serializers.ModelSerializer):
    class Meta:
        model = DominoTeam
        exclude = ['team_id', 'game', 'team_name']
