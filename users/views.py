from django.shortcuts import render
from users.models import User
from rest_framework import viewsets
from .serializers import CustomRegisterSerializer, UserSerializer
from .models import User, Patient

class RegisterView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    