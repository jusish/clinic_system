from django.db import models
from patients.models import Patient
from authentication.models import Doctor
from billing.models import BillingRecord
from inventory.models import Medicine, MedicineDispense
from medical_records.models import MedicalRecord

class MLPrediction(models.Model):
    """Store ML predictions for future reference and evaluation"""
    PREDICTION_TYPES = [
        ('READMISSION', 'Readmission Risk'),
        ('COST', 'Treatment Cost Prediction'),
        ('INVENTORY', 'Inventory Depletion Prediction'),
        ('APPOINTMENT', 'Appointment No-Show Prediction'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    prediction_type = models.CharField(max_length=20, choices=PREDICTION_TYPES)
    prediction_value = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)
    confidence_score = models.FloatField()
    features_used = models.JSONField()  # Store the features used for this prediction
    
    def __str__(self):
        if self.patient:
            return f"{self.get_prediction_type_display()} for {self.patient.name}"
        elif self.medicine:
            return f"{self.get_prediction_type_display()} for {self.medicine.name}"
        else:
            return f"{self.get_prediction_type_display()} general prediction"

class FeatureStore(models.Model):
    """Store preprocessed features for ML models"""
    feature_name = models.CharField(max_length=100)
    feature_value = models.FloatField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['feature_name']),
            models.Index(fields=['patient']),
            models.Index(fields=['medicine']),
        ]
