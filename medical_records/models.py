from django.db import models
from patients.models import Patient
from authentication.models import Doctor

class MedicalRecord(models.Model):

    CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('FOLLOW_UP', 'Follow Up Required')
    ]


    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)