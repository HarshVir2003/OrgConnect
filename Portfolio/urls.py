from django.urls import path
from Portfolio.views import PortfolioView, PortfolioPostView

urlpatterns = [
    path('', PortfolioPostView.as_view(), name='portfolio-list'),
    path('<int:id>/', PortfolioView.as_view(), name='portfolio-detail'),

]