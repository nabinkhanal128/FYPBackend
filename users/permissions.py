from django.contrib.auth.models import User
from rest_framework import permissions

from users import models
from users.models import CustomUser, Patient, Doctor

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any permissions are only allowed to the owner of the meeting
        return obj.user == request.user

class PatientOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any permissions are only allowed to the owner of the meeting
        return Patient.user == request.user
class DoctorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any permissions are only allowed to the owner of the meeting
        return obj.user == request.user.is_doctor