import jwt
from django.shortcuts import render

# Create your views here.
from jwt import ExpiredSignatureError
from rest_framework.response import Response
from requests import exceptions
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from FYPBackend import settings
from appointment.models import Appointment, AppointmentReport
from appointment.serializers import AppointmentSerializer, FeedbackResponseSerializer
from users.models import CustomUser, Doctor, Patient
from users.permissions import DoctorOrReadOnly


class AppointmentViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('doctor__specialization', 'doctor__first_name', 'appointment_time',)

    def list(self, request):
        if request.user.is_active==False:
            queryset = Appointment.objects.all()
        elif request.user.is_doctor:
            queryset = Appointment.objects.filter(doctor=Doctor.objects.get(user=self.request.user))
            serializer = AppointmentSerializer(queryset, many=True, )
            print(serializer)
        elif request.user.is_active:
            queryset = Appointment.objects.all()
            serializer = AppointmentSerializer(queryset, many=True, )
        else:
            queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many=True, )
        return Response(serializer.data)

    def create(self, request):
        if self.request.user.is_doctor:
            serializer = AppointmentSerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save(doctor=Doctor.objects.get(user=self.request.user))
            print(serializer)
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

    def list(self, request):
        if request.user.is_active==False:
            return Response({'error': 'Login to view your personal report.'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.is_doctor:
            queryset = AppointmentReport.objects.filter(report_by=Doctor.objects.get(user=self.request.user))
            serializer = FeedbackResponseSerializer(queryset, many=True, )
        elif request.user.is_patient:
            queryset = AppointmentReport.objects.filter(response_to=Patient.objects.get(user=self.request.user))
            serializer = FeedbackResponseSerializer(queryset, many=True, )
        else:
            return Response({'Error': 'Invalid access'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FeedbackResponseSerializer(queryset, many=True, )
        return Response(serializer.data)

    def create(self, request):
        if self.request.user.is_doctor:
            serializer = AppointmentSerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            print(serializer)
            return Response({'success': 'Successfully Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Only verified doctors can create'}, status=status.HTTP_400_BAD_REQUEST)