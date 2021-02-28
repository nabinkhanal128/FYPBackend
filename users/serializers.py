from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Doctor
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'profile_pic', 'phone_number', 'dob', 'password')
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
            address=validated_data['address'],
            profile_pic=validated_data['profile_pic'],
            dob=validated_data['dob'],
            phone_number=validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user



class showProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = CustomUser
      fields = "__all__"

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
