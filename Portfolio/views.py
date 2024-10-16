from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Portfolio.models import PortfolioModel
from Portfolio.Serializer import PortfolioSerializer


class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            try:
                portfolio = PortfolioModel.objects.get(id=id)
                serializer = PortfolioSerializer(portfolio)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PortfolioModel.DoesNotExist:
                return Response({"error": "Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            portfolios = PortfolioModel.objects.all()
            serializer = PortfolioSerializer(portfolios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            portfolio = PortfolioModel.objects.get(id=id, user_id=request.user)
        except PortfolioModel.DoesNotExist:
            return Response({"error": "Portfolio not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
