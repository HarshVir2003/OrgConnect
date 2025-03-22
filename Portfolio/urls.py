# from django.urls import path
# from Portfolio.views import PortfolioViewSet
#
# urlpatterns = [
#     path('', PortfolioViewSet.as_view(), name='portfolio-list'),
#     # path('<int:id>/', PortfolioView.as_view(), name='portfolio-detail'),
#
# ]

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, PortfolioIdView

router = DefaultRouter()
router.register(r'', PortfolioViewSet, basename='portfolio')

urlpatterns = router.urls + [
    path('get/id', PortfolioIdView.as_view())
]
