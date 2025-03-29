# ml_system/feature_engineering.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Sum, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay

from patients.models import Patient
from billing.models import BillingRecord
from inventory.models import Medicine, MedicineDispense
from medical_records.models import MedicalRecord
from ml_system.models import FeatureStore

def calculate_patient_age(patient):
    """Calculate patient age in years"""
    today = datetime.now().date()
    born = patient.dob
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def extract_patient_features():
    """Extract and create features for each patient"""
    patients = Patient.objects.all()
    
    for patient in patients:
        # Basic demographic features
        age = calculate_patient_age(patient)
        
        # Visit frequency features
        current_date = datetime.now().date()
        records = MedicalRecord.objects.filter(patient=patient)
        visit_count = records.count()
        
        if visit_count > 0:
            last_visit = records.order_by('-date').first().date.date()
            days_since_last_visit = (current_date - last_visit).days
            avg_days_between_visits = 0
            
            if visit_count > 1:
                sorted_visits = list(records.order_by('date').values_list('date', flat=True))
                intervals = [(sorted_visits[i+1] - sorted_visits[i]).days for i in range(len(sorted_visits)-1)]
                avg_days_between_visits = sum(intervals) / len(intervals)
        else:
            days_since_last_visit = 0
            avg_days_between_visits = 0
        
        # Billing features
        billings = BillingRecord.objects.filter(patient=patient)
        avg_bill_amount = billings.aggregate(Avg('total_cost'))['total_cost__avg'] or 0
        total_billed = billings.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        
        # Treatment complexity features
        diagnosis_length = sum(len(record.diagnosis) for record in records) / max(1, visit_count)
        treatment_length = sum(len(record.treatment) for record in records) / max(1, visit_count)
        
        # Store features
        feature_mappings = {
            'patient_age': age,
            'visit_count': visit_count,
            'days_since_last_visit': days_since_last_visit,
            'avg_days_between_visits': avg_days_between_visits,
            'avg_bill_amount': avg_bill_amount,
            'total_billed': total_billed,
            'diagnosis_complexity': diagnosis_length,
            'treatment_complexity': treatment_length,
        }
        
        # Save features to the FeatureStore
        for feature_name, feature_value in feature_mappings.items():
            FeatureStore.objects.update_or_create(
                patient=patient,
                feature_name=feature_name,
                defaults={'feature_value': feature_value}
            )

def extract_medicine_features():
    """Extract and create features for medicine inventory"""
    medicines = Medicine.objects.all()
    
    for medicine in medicines:
        # Usage pattern features
        dispenses = MedicineDispense.objects.filter(medicine=medicine)
        dispense_count = dispenses.count()
        
        if dispense_count > 0:
            total_dispensed = dispenses.aggregate(Sum('quantity_dispensed'))['quantity_dispensed__sum'] or 0
            avg_dispensed = total_dispensed / dispense_count
            
            # Time-based patterns
            last_month_dispensed = dispenses.filter(
                date__gte=datetime.now() - timedelta(days=30)
            ).aggregate(Sum('quantity_dispensed'))['quantity_dispensed__sum'] or 0
            
            # Calculate depletion rate
            current_quantity = medicine.quantity
            depletion_rate = last_month_dispensed / 30  # Daily usage rate
            days_until_depletion = float('inf') if depletion_rate == 0 else current_quantity / depletion_rate
        else:
            avg_dispensed = 0
            last_month_dispensed = 0
            depletion_rate = 0
            days_until_depletion = float('inf')
        
        # Store features
        feature_mappings = {
            'dispense_count': dispense_count,
            'avg_dispensed': avg_dispensed,
            'last_month_dispensed': last_month_dispensed,
            'depletion_rate': depletion_rate,
            'days_until_depletion': min(days_until_depletion, 9999),  # Cap at a reasonable value
            'current_quantity': medicine.quantity,
        }
        
        # Save features to the FeatureStore
        for feature_name, feature_value in feature_mappings.items():
            FeatureStore.objects.update_or_create(
                medicine=medicine,
                feature_name=feature_name,
                defaults={'feature_value': feature_value}
            )

def extract_all_features():
    """Extract all features and store them"""
    extract_patient_features()
    extract_medicine_features()
    return True
