from django.contrib import admin

# Register your models here.
from booking.models import AppointmentBook, Insight

admin.register(AppointmentBook)
admin.register(Insight)