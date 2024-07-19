from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackingDataViewSet

router = DefaultRouter()
router.register(r'tracking-data', TrackingDataViewSet,basename='Tracking data')

urlpatterns = [
    path('', include(router.urls)),
]