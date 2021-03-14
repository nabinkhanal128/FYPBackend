from django.db import models

# Create your models here.


class Appointment(models.Model):
    doctor = models.ForeignKey("users.Doctor", on_delete=models.CASCADE)
    appointment_date= models.DateField(auto_now=False, auto_now_add=False)
    appointment_time= models.DateField(auto_now=False, auto_now_add=False)
    appointment_details = models.CharField(max_length=1000)

    @property
    def owner(self):
        return self.doctor



class AppointmentReport(models.Model):
    response_to = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    report_by = models.ForeignKey('users.Doctor', on_delete=models.CASCADE)
    report_detail = models.TextField()
    status = models.TextField()
    medication_description = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)


