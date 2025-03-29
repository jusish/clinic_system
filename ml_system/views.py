# ml_system/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from ml_system.services import generate_all_predictions, get_dashboard_predictions
from ml_system.models import MLPrediction
from patients.models import Patient
from inventory.models import Medicine

@login_required
def generate_predictions(request):
    """View to trigger prediction generation"""
    generate_all_predictions()
    return redirect('dashboard')

@login_required
def get_predictions_api(request):
    """API to get predictions for dashboard"""
    predictions = get_dashboard_predictions()
    return JsonResponse(predictions)

@login_required
def patient_prediction_detail(request, patient_id):
    """View to show detailed predictions for a patient"""
    patient = Patient.objects.get(id=patient_id)
    predictions = MLPrediction.objects.filter(
        patient=patient
    ).order_by('-prediction_date')[:10]
    
    context = {
        'patient': patient,
        'predictions': predictions
    }
    return render(request, 'ml_system/patient_prediction_detail.html', context)

@login_required
def medicine_prediction_detail(request, medicine_id):
    """View to show detailed predictions for a medicine"""
    medicine = Medicine.objects.get(id=medicine_id)
    predictions = MLPrediction.objects.filter(
        medicine=medicine
    ).order_by('-prediction_date')[:10]
    
    context = {
        'medicine': medicine,
        'predictions': predictions
    }
    return render(request, 'ml_system/medicine_prediction_detail.html', context)