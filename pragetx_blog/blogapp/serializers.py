from rest_framework import serializers
from .models import trackingData

class TrackingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = trackingData
        fields = '__all__'