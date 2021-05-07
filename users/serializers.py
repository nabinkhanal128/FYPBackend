from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers, status, validators
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Doctor, Patient
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'dob', 'address','gender_type',
                  'user_type', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True},
                        'email': {'required': True, 'validators': [EmailValidator, ]},
                        }

    def create(self, validated_data):
        """ Creates and returns a new user """

        # Validating Data
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            dob = validated_data['dob'],
            address = validated_data['address'],
            gender_type = validated_data['gender_type'],
            user_type = validated_data['user_type']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = fields = ('first_name', 'last_name', 'phone_number', 'dob', 'address','gender_type')

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    email = serializers.ReadOnlyField(source="user.email")
    phone_number = serializers.ReadOnlyField(source="user.phone_number")
    dob = serializers.ReadOnlyField(source="user.dob")
    address = serializers.ReadOnlyField(source="user.address")
    gender_type = serializers.ReadOnlyField(source="user.gender_type")
    class Meta:
        model = Patient
        fields = ('user', 'first_name', 'last_name', 'email', 'phone_number', 'dob', 'address',
                  'gender_type', 'blood_type', 'profile_pic')

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    email = serializers.ReadOnlyField(source="user.email")
    phone_number = serializers.ReadOnlyField(source="user.phone_number")
    dob = serializers.ReadOnlyField(source="user.dob")
    address = serializers.ReadOnlyField(source="user.address")
    gender_type = serializers.ReadOnlyField(source="user.gender_type")
    class Meta:
        model = Doctor
        fields = ('user', 'first_name', 'last_name', 'email', 'phone_number', 'dob', 'address', 'gender_type',
                  'specialization', 'about','profile_pic')

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
            data['user_type'] = str(self.user.user_type)
            data["user_id"] = int(self.user.pk)
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
