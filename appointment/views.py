import jwt
from django.shortcuts import render

# Create your views here.
from jwt import ExpiredSignatureError
from rest_framework.response import Response
from requests import exceptions
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from FYPBackend import settings
from appointment.models import Appointment, AppointmentReport
from appointment.serializers import AppointmentSerializer, FeedbackResponseSerializer
from users.models import CustomUser, Doctor
from users.permissions import DoctorOrReadOnly


class AppointmentViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def list(self, request):
        if request.user.is_active:
            queryset = Appointment.objects.filter(doctor=Doctor.objects.get(user=self.request.user))
            serializer = AppointmentSerializer(queryset, many=True, )
        else:
            queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many=True, )
        return Response(serializer.data)

    def perform_create(self, serializer):
        if self.request.user.is_doctor:
            serializer.is_valid()
            serializer.save(user=Doctor.objects.get(user=self.request.user))
            return Response({'success': 'Successfully Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Only verified doctors can create'}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        return super(AppointmentViewset, self).get_permissions()



class ResponseViewset(viewsets.ModelViewSet):
    serializer_class = FeedbackResponseSerializer
    queryset = AppointmentReport.objects.all()