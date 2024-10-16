from django.urls import path
from Portfolio.views import PortfolioView

urlpatterns = [
    path('', PortfolioView.as_view(), name='portfolio-list'),
    path('<int:id>/', PortfolioView.as_view(), name='portfolio-detail'),
]