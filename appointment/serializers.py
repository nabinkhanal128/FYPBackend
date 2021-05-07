from rest_framework import serializers

from appointment.models import Appointment, AppointmentReport
from users.serializers import DoctorSerializer, UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = ('doctor', 'appointment_date', 'appointment_time', 'appointment_details', 'price')


class FeedbackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentReport
        fields = '__all__'