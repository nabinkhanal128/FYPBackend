from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from users.models import Patient, Doctor
from users.permissions import PatientOrReadOnly
from .models import AppointmentBook, Insight
from .serializers import AppointmentBookSerializer, InsightSerializer
from rest_framework import viewsets, status


class AppointmentBookViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentBookSerializer
    queryset = AppointmentBook.objects.all()

    def list(self, request):
        if request.user.is_active==False:
            return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.is_doctor:
            queryset = AppointmentBook.objects.filter(doctor=Doctor.objects.get(user=self.request.user))
            serializer = AppointmentBookSerializer(queryset, many=True, )
        elif request.user.is_active:
            queryset = AppointmentBook.objects.all()
            serializer = AppointmentBookSerializer(queryset, many=True, )
        else:
            queryset = AppointmentBook.objects.all()
        serializer = AppointmentBookSerializer(queryset, many=True, )
        return Response(serializer.data)

    def create(self, request):
        if self.request.user.is_patient:
            serializer = AppointmentBookSerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            return Response({'success': 'Successfully Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, url_path='booked')
    def get_treatment(self, request, pk=None):
        appointment = self.get_object()
        try:
            booked = AppointmentBook.objects.get(appointment=appointment)
            serializer = self.get_serializer(booked)
            return Response(serializer.data)
        except AppointmentBook.DoesNotExist:
            return Response({'detail': 'No Booking Found for selected Appointment'}, status=HTTP_404_NOT_FOUND)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        return super(AppointmentBookViewset, self).get_permissions()

class InsightViewset(viewsets.ModelViewSet):
    serializer_class = InsightSerializer
    queryset = Insight.objects.all()