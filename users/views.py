import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets, status, views, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Doctor, Patient, CustomUser
from users.serializers import PatientSerializer, DoctorSerializer, UserSerializer, CustomTokenObtainPairSerializer, \
    EmailVerificationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

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

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            user=CustomUser.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            absurl = 'http://' + str(current_site) + relativeLink
            email_body = 'Hello ' + user.first_name + ' Use below link to reset your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password!'}
            Util.send_email(data)
        return Response({'success':'Reset password link has been sent!'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token request new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials Valid','uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)


        except DjangoUnicodeDecodeError as identified:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Invalid token request new one'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny, ]
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password reset was successful'}, status = status.HTTP_200_OK)