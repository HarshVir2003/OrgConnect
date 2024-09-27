from rest_framework import serializers
from Achievements.models import Achievements


class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'
