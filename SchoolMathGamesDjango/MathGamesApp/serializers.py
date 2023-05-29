from rest_framework import serializers
from .models import *


class AbakaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbakaTeam
        fields = '__all__'


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusTeam
        fields = '__all__'


class DominoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DominoTeam
        fields = '__all__'
