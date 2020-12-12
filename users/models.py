from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_clinic = models.BooleanField()
    is_doctor = models.BooleanField()
    is_patient = models.BooleanField()

    def __str__(self):
        return self.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
