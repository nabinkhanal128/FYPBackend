from rest_framework import serializers
from .models import AppointmentBook, Insight

class AppointmentBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentBook
        fields = ('__all__')

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ('__all__')