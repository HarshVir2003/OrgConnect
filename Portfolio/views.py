# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from Portfolio.models import PortfolioModel
# from Portfolio.Serializer import PortfolioSerializer
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
#
#
# class PortfolioView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     @swagger_auto_schema(
#         operation_summary='GET Portfolio from id',
#         manual_parameters=[
#             openapi.Parameter(
#                 'id',  # the name of the path parameter
#                 openapi.IN_PATH,  # location of the parameter (in the path)
#                 type=openapi.TYPE_INTEGER,  # define the parameter type as string
#                 description="A unique string value identifying this user",  # parameter description
#                 required=True,  # specify that it's required
#             )
#         ],
#         operation_description='GET portfolio from id, if id is not passed, then portfolio of current user is retured if'
#                               ' a user is logged in.',
#         responses={200: 'valid portfolio',
#                    404: 'no portfolio found.',
#                    405: 'no id passed.'},
#         # request_body=openapi.Schema(
#         #     type=openapi.TYPE_OBJECT,
#         #     properties={
#         #         'bio': openapi.Schema(type=openapi.TYPE_STRING),
#         #         'location': openapi.Schema(type=openapi.TYPE_STRING),
#         #         'website': openapi.Schema(type=openapi.TYPE_OBJECT),
#         #         'birth_date': openapi.Schema(type=openapi.TYPE_STRING),
#         #         'linkedin_url': openapi.Schema(type=openapi.TYPE_STRING),
#         #         'github_url': openapi.Schema(type=openapi.TYPE_STRING),
#         #         'kaggle_url': openapi.Schema(type=openapi.TYPE_STRING),
#         #         'google_scholar_url': openapi.Schema(type=openapi.TYPE_STRING),
#         #     }
#         # )
#     )
#     def get(self, request, id=None):
#         try:
#             portfolio = PortfolioModel.objects.get(id=id)
#             serializer = PortfolioSerializer(portfolio)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except PortfolioModel.DoesNotExist:
#             return Response({"error": "Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
#
#     @swagger_auto_schema(
#         operation_summary='PUT to update a portfolio.',
#         responses={
#             200: 'status ok',
#             400: 'invalid data, bad request',
#             404: 'Portfolio not found or unauthorized'
#         }
#     )
#     def put(self, request, id=None):
#         try:
#             portfolio = PortfolioModel.objects.get(id=id, user_id=request.user)
#         except PortfolioModel.DoesNotExist:
#             return Response({"error": "Portfolio not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(
#         operation_summary='DELETE portfolio by id.',
#         responses={
#             204: 'Portfolio deleted',
#             404: 'Portfolio not found or unauthorized.'
#         }
#     )
#     def delete(self, request, id=None):
#         try:
#             PortfolioModel.objects.get(id=id, user_id=request.user)
#         except PortfolioModel.DoesNotExist:
#             return Response({"error": "Portfolio not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
#
#         PortfolioModel.objects.filter(id=id, user_id=request.user).delete()
#         return Response({'message': f'Portfolio for user {request.user.username} deleted.'},
#                         status=status.HTTP_204_NO_CONTENT)
#
#
# class PortfolioPostView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     @swagger_auto_schema(
#         operation_summary='POST create portfolio.',
#         request_body=PortfolioSerializer
#     )
#     def post(self, request):
#         serializer = PortfolioSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user_id=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

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
