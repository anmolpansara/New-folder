from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import trackingData
from .serializers import TrackingDataSerializer
from blogapp.customs.viewsets import CustomStatusTrue, CustomViewSetMaster


class TrackingDataViewSet(CustomViewSetMaster):
    queryset = trackingData.objects.all()
    serializer_class = TrackingDataSerializer
