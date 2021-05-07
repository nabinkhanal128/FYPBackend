from rest_framework import serializers
from .models import AppointmentBook, Insight


class AppointmentBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentBook
        fields = ('appointment', 'patient', 'book')


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ('__all__')
