from django.contrib import admin

# Register your models here.
from booking.models import AppointmentBook, Insight

admin.site.register(AppointmentBook)
admin.site.register(Insight)