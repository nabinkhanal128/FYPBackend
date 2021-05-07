from django.contrib import admin

# Register your models here.
from appointment.models import Appointment, AppointmentReport

admin.site.register(Appointment)
admin.site.register(AppointmentReport)
