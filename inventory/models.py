from django.db import models

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

class MedicineDispense(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_dispensed = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
