from rest_framework import serializers

from appointment.models import Appointment, AppointmentReport

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['doctor']


class FeedbackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentReport
        fields = '__all__'