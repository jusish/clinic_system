from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    contact_info = models.CharField(max_length=100)
    date_attended = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name