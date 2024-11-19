from django.db import models
from django.contrib.auth.models import AbstractUser

class Doctor(AbstractUser):
    
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
    ]
    
    specialization = models.CharField(choices=SPECIALIZATION_CHOICES, max_length=200)

    def __str__(self):
        return f'{self.username} - {self.specialization}'
    
    
    class Meta:
        db_table = 'users'
