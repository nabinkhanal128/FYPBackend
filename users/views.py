from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets, serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Doctor, Patient, CustomUser
from users.serializers import PatientSerializer, DoctorSerializer, UserSerializer, CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    def create(self,request):
        serialier=UserSerializer(data=request.data,context={"request":request})
        serialier.is_valid()
        serialier.save()
        return Response({"error":"False","message":"New Data Created"})

    def list(self, request):
        post = CustomUser.objects.all()
        serializer = UserSerializer(post, many=True, context={"request": request})
        return Response(serializer.data)

class PatientViewset(viewsets.ViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny, ]
    def create(self,request):
        serialier=PatientSerializer(data=request.data,context={"request":request})
        serialier.is_valid()
        serialier.save()
        return Response({"error":"False","message":"New Data Created"})
    def list(self, request):
        post = Patient.objects.all()
        serializer = PatientSerializer(post, many=True, context={"request": request})
        return Response(serializer.data)

class DoctorViewset(viewsets.ViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny, ]
    def create(self,request):
        serialier=DoctorSerializer(data=request.data,context={"request":request})
        serialier.is_valid()
        serialier.save()
        return Response({"error":"False","message":"New Data Created"})
    def list(self, request):
        post = Doctor.objects.all()
        serializer = DoctorSerializer(post, many=True, context={"request": request})
        return Response(serializer.data)

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

