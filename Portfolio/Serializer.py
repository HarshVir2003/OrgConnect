from rest_framework import serializers
from Portfolio.models import PortfolioModel


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioModel
        fields = [
            'bio',
            'location',
            'website',
            'birth_date',
            'linkedin_url',
            'github_url',
            'kaggle_url',
            'google_scholar_url',
        ]

    def create(self, validated_data):
        portfolio_object = PortfolioModel.objects.create(**validated_data)
        return portfolio_object

