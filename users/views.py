import os
from django.http import HttpResponsePermanentRedirect
from rest_framework import viewsets, generics, status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Doctor, Patient, CustomUser
from users.serializers import PatientSerializer, DoctorSerializer, UserSerializer, CustomTokenObtainPairSerializer, \
    EmailVerificationSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny, ]
    def create(self, request):
        serializer=UserSerializer(data=request.data,context={"request": request})
        serializer.is_valid()
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relativeLink = reverse('email-verify')
        absurl = 'http://'+str(current_site)+relativeLink+'>token='+str(token)
        email_body='Hello '+user.first_name+' Use below link to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your Email!'}
        Util.send_email(data)
        return Response(user_data, status= status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user=CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Token has been expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token request new one'}, status=status.HTTP_400_BAD_REQUEST)




class PatientViewset(viewsets.ViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny, ]
    def create(self,request):
        serializer=PatientSerializer(data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
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
        serializer=DoctorSerializer(data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":"False","message":"New Data Created"})
    def list(self, request):
        post = Doctor.objects.all()
        serializer = DoctorSerializer(post, many=True, context={"request": request})
        return Response(serializer.data)

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

