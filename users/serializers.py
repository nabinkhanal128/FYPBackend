from rest_framework import serializers
from .models import User
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_clinic', 'is_doctor', 'is_patient')

class CustomRegisterSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_clinic', 'is_doctor', 'is_patient')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_clinic': self.validated_data.get('is_clinic', ''),
            'is_doctor': self.validated_data.get('is_doctor', ''),
            'is_patient': self.validated_data.get('is_patient', ''),
        }


    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_clinic = self.cleaned_data.get('is_clinic')
        user.is_doctor = self.cleaned_data.get('is_doctor')
        user.is_patient = self.cleaned_data.get('is_patient')
        adapter.save_user(request, user, self)
        return user