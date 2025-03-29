# ml_system/ml_models.py
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

from ml_system.models import FeatureStore, MLPrediction
from patients.models import Patient
from inventory.models import Medicine
import os

class ReadmissionPredictor:
    """Predict patient readmission risk"""
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = 'ml_models/readmission_model.joblib'
        self.scaler_path = 'ml_models/readmission_scaler.joblib'
        self.features = [
            'patient_age', 'visit_count', 'days_since_last_visit',
            'avg_days_between_visits', 'avg_bill_amount', 'diagnosis_complexity',
            'treatment_complexity'
        ]
    
    def train(self):
        """Train the readmission prediction model"""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        # Get unique patients
        patients = Patient.objects.all()
        
        # Prepare training data
        X = []
        y = []
        
        for patient in patients:
            # Get features for this patient
            patient_features = {}
            for feature in self.features:
                try:
                    feature_obj = FeatureStore.objects.get(patient=patient, feature_name=feature)
                    patient_features[feature] = feature_obj.feature_value
                except FeatureStore.DoesNotExist:
                    patient_features[feature] = 0
            
            # Create feature vector
            feature_vector = [patient_features[f] for f in self.features]
            X.append(feature_vector)
            
            # Create target variable (readmission within 30 days)
            # For demonstration, we'll use a heuristic based on visit frequency
            visits = patient_features['visit_count']
            days_since = patient_features['days_since_last_visit']
            
            # Patients with high visit count and recent visits are more likely to be readmitted
            readmission_risk = 1 if visits > 3 and days_since < 60 else 0
            y.append(readmission_risk)
        
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model and scaler
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        return accuracy
    
    def load(self):
        """Load the trained model"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        except:
            return False
    
    def predict(self, patient_id):
        """Make predictions for a patient"""
        try:
            # Get patient
            patient = Patient.objects.get(id=patient_id)
            
            # Get features
            patient_features = {}
            for feature in self.features:
                try:
                    feature_obj = FeatureStore.objects.get(patient=patient, feature_name=feature)
                    patient_features[feature] = feature_obj.feature_value
                except FeatureStore.DoesNotExist:
                    patient_features[feature] = 0
            
            # Create feature vector
            feature_vector = np.array([[patient_features[f] for f in self.features]])
            
            # Scale features
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Make prediction
            probability = self.model.predict_proba(feature_vector_scaled)[0, 1]
            
            # Store prediction
            MLPrediction.objects.create(
                patient=patient,
                prediction_type='READMISSION',
                prediction_value=probability,
                confidence_score=probability,
                features_used=patient_features
            )
            
            return probability
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

class InventoryPredictionModel:
    """Predict inventory depletion and future needs"""
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = 'ml_models/inventory_model.joblib'
        self.scaler_path = 'ml_models/inventory_scaler.joblib'
        self.features = [
            'dispense_count', 'avg_dispensed', 'last_month_dispensed',
            'depletion_rate', 'current_quantity'
        ]
    
    def train(self):
        """Train the inventory prediction model"""
        # Get unique medicines
        medicines = Medicine.objects.all()
        
        # Prepare training data
        X = []
        y = []
        
        for medicine in medicines:
            # Get features for this medicine
            medicine_features = {}
            for feature in self.features:
                try:
                    feature_obj = FeatureStore.objects.get(medicine=medicine, feature_name=feature)
                    medicine_features[feature] = feature_obj.feature_value
                except FeatureStore.DoesNotExist:
                    medicine_features[feature] = 0
            
            # Create feature vector
            feature_vector = [medicine_features[f] for f in self.features]
            X.append(feature_vector)
            
            # Create target variable (days until depletion)
            days_until_depletion = medicine_features.get('days_until_depletion', 30)
            y.append(days_until_depletion)
        
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        
        # Save model and scaler
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        return mse
    
    def load(self):
        """Load the trained model"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        except:
            return False
    
    def predict(self, medicine_id):
        """Make predictions for a medicine"""
        try:
            # Get medicine
            medicine = Medicine.objects.get(id=medicine_id)
            
            # Get features
            medicine_features = {}
            for feature in self.features:
                try:
                    feature_obj = FeatureStore.objects.get(medicine=medicine, feature_name=feature)
                    medicine_features[feature] = feature_obj.feature_value
                except FeatureStore.DoesNotExist:
                    medicine_features[feature] = 0
            
            # Create feature vector
            feature_vector = np.array([[medicine_features[f] for f in self.features]])
            
            # Scale features
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Make prediction
            days_until_depletion = self.model.predict(feature_vector_scaled)[0]
            confidence = 0.8  # Simplified confidence measure
            
            # Store prediction
            MLPrediction.objects.create(
                medicine=medicine,
                prediction_type='INVENTORY',
                prediction_value=days_until_depletion,
                confidence_score=confidence,
                features_used=medicine_features
            )
            
            return days_until_depletion
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
