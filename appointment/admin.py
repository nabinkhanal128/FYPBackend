from django.contrib import admin

# Register your models here.
from appointment.models import Appointment, AppointmentReport

admin.register(Appointment)
admin.register(AppointmentReport)
