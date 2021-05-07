from django.db import models

# Create your models here.

class AppointmentBook(models.Model):
    appointment = models.ForeignKey("appointment.Appointment", on_delete=models.CASCADE)
    patient = models.ForeignKey("users.Patient", on_delete=models.CASCADE)
    book = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def owner(self):
        return self.patient


class Insight(models.Model):
    appointment = models.ForeignKey("appointment.Appointment", on_delete=models.CASCADE)
    booking_cancel_probability = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)