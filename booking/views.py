from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from users.permissions import PatientOrReadOnly
from .models import AppointmentBook, Insight
from .serializers import AppointmentBookSerializer, InsightSerializer
from rest_framework import viewsets

class AppointmentBookViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentBookSerializer
    queryset = AppointmentBook.objects.all()
    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated, PatientOrReadOnly)
        if self.request.method == 'PUT':
            self.permission_classes = (PatientOrReadOnly,)
        if self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated, PatientOrReadOnly,)
        return super(AppointmentBookViewset, self).get_permissions()

class InsightViewset(viewsets.ModelViewSet):
    serializer_class = InsightSerializer
    queryset = Insight.objects.all()