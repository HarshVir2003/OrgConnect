from rest_framework import serializers
from Portfolio.models import PortfolioModel


class PortfolioSerializer(serializers.Serializer):
    class Meta:
        model = PortfolioModel
        fields = '__all__'
