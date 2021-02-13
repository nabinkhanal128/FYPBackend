from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Patient, Doctor
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True},
                        'email': {'required': True}, }

    def create(self, validated_data):
        """ Creates and returns a new user """

        # Validating Data
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = CustomUser.USERNAME_FIELD

class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        if self.user.is_verified == True:
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
        else:
            raise serializers.ValidationError("Email should be validated!!")

        return data

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=4)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):

    password= serializers.CharField(min_length=8, max_length=40, write_only=True)
    token= serializers.CharField(min_length=1, write_only=True)
    uidb64= serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user= CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid!', 401)

            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid!', 401)
        return super().validate(attrs)
