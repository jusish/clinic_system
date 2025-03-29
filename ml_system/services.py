from ml_system.feature_engineering import extract_all_features
from ml_system.ml_models import ReadmissionPredictor, InventoryPredictionModel
from ml_system.models import MLPrediction
from patients.models import Patient
from inventory.models import Medicine

def generate_all_predictions():
    """Generate predictions for all patients and medicines"""
    # Extract features
    extract_all_features()
    
    # Initialize predictors
    readmission_predictor = ReadmissionPredictor()
    inventory_predictor = InventoryPredictionModel()
    
    # Check if models exist, if not train them
    if not readmission_predictor.load():
        readmission_predictor.train()
    
    if not inventory_predictor.load():
        inventory_predictor.train()
    
    # Generate readmission predictions for all patients
    patients = Patient.objects.all()
    for patient in patients:
        readmission_predictor.predict(patient.id)
    
    # Generate inventory predictions for all medicines
    medicines = Medicine.objects.all()
    for medicine in medicines:
        inventory_predictor.predict(medicine.id)
    
    return True

def get_dashboard_predictions():
    """Get predictions formatted for dashboard display"""
    # Get latest readmission predictions
    high_risk_patients = MLPrediction.objects.filter(
        prediction_type='READMISSION',
        prediction_value__gte=0.7
    ).order_by('-prediction_date')[:5]
    
    # Get latest inventory predictions
    low_stock_medicines = MLPrediction.objects.filter(
        prediction_type='INVENTORY',
        prediction_value__lte=14  # Less than 14 days until depletion
    ).order_by('prediction_value')[:5]
    
    # Format data for dashboard
    patient_risk_data = [{
        'id': pred.patient.id,
        'name': pred.patient.name,
        'risk_score': round(pred.prediction_value * 100, 1),
        'last_visit': pred.patient.date_attended.strftime('%Y-%m-%d')
    } for pred in high_risk_patients]
    
    inventory_data = [{
        'id': pred.medicine.id,
        'name': pred.medicine.name,
        'days_remaining': round(pred.prediction_value, 1),
        'current_quantity': pred.medicine.quantity
    } for pred in low_stock_medicines]
    
    return {
        'patient_risk_data': patient_risk_data,
        'inventory_data': inventory_data
    }
