from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import Portfolio
from .Serializer import PortfolioSerializer
from rest_framework.generics import ListAPIView


class PortfolioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def list(self, request):
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolios, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk, user=request.user)
        except Portfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PortfolioSerializer(portfolio, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # Ensure portfolio belongs to logged-in user
        obj = Portfolio.objects.filter(user=request.user.id)
        if obj.exists():
            return Response({'message': "Portfolio for user already exists."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PortfolioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk, user_id=request.user)
        except Portfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        serializer = PortfolioSerializer(portfolio, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk, user=request.user)
        except Portfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)

        portfolio.delete()
        return Response({'message': 'Portfolio deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class PortfolioIdView(ListAPIView):
    queryset = Portfolio.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        portfolio = queryset.filter(user=request.user)
        if portfolio.exists():
            return Response({'PortfolioId': portfolio[0].id}, status=status.HTTP_200_OK)
        return Response({'PortfolioId': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
