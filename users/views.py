import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets, status, views, generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Doctor, CustomUser
from users.serializers import DoctorSerializer, UserSerializer, CustomTokenObtainPairSerializer, \
    EmailVerificationSerializer, ChangePasswordSerializer, showProfileSerializer
from .permissions import OwnProfilePermission
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.shortcuts import get_object_or_404

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
        absurl = 'http://'+str(current_site)+relativeLink+'?token='+str(token)
        email_body='Hello '+user.first_name+' Use below link to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your Email!'}
        Util.send_email(data)
        return Response(user_data, status= status.HTTP_201_CREATED)



class ProfileAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['user_id'])
        profile_serializer = UserSerializer()
        return Response(profile_serializer.data)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
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



class DoctorViewset(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminUser, OwnProfilePermission, ]




class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class ShowProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = showProfileSerializer(request.user)
        return Response(serializer.data)