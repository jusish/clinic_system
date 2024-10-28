from django.db import models

# Create your models here.
from patients.models import Patient

class BillingRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
