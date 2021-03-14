from django.db import models

# Create your models here.

class AppointmentBook(models.Model):
    appointment = models.ForeignKey("appointment.Appointment", on_delete=models.CASCADE, primary_key=True)
    appointment_for = models.ForeignKey("users.Patient", on_delete=models.CASCADE)
    payment_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient_appointment} by {self.appointment_for}'

class Insight(models.Model):
    appointment = models.ForeignKey("appointment.Appointment", on_delete=models.CASCADE, primary_key=True)
    booking_cancel_probability = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)