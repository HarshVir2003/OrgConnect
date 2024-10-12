from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from Portfolio.models import PortfolioModel
from Portfolio.Serializer import PortfolioSerializer


# Create your views here.
class PortfolioView(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    queryset = PortfolioModel.objects.all()
    lookup_field = 'id'
    serializer_class = PortfolioSerializer
