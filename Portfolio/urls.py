from django.urls import path
from Portfolio.views import PortfolioView

urlpatterns = [
    path('portfolio/', PortfolioView.as_view(), name='portfolio-list'),
    path('portfolio/<int:id>/', PortfolioView.as_view(), name='portfolio-detail'),
]