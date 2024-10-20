from rest_framework import serializers
from Portfolio.models import PortfolioModel


class PortfolioSerializer(serializers.Serializer):

    def validate(self, attrs):
        try:
            date = attrs['birth_date']
            bio = attrs['bio']
            return attrs
        except KeyError:
            raise serializers.ValidationError("NO birth date provided!")

    def create(self, validated_data):
        portfolio_object = PortfolioModel.objects.create(**validated_data)
        return portfolio_object

    class Meta:
        model = PortfolioModel
        fields = '__all__'
