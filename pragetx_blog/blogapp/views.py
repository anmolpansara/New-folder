from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import trackingData
from .serializers import TrackingDataSerializer

class TrackingDataViewSet(viewsets.ModelViewSet):
    queryset = trackingData.objects.all()
    serializer_class = TrackingDataSerializer
