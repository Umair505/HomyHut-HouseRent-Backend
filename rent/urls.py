from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentAdvertisementViewSet, RentRequestViewSet

router = DefaultRouter()
router.register('rent-ads', RentAdvertisementViewSet, basename='rent-ads')
router.register('rent-requests', RentRequestViewSet, basename='rent-requests')

urlpatterns = [
    path('', include(router.urls)),
]