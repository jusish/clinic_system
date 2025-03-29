# ml_system/urls.py
from django.urls import path
from ml_system import views

app_name = 'predictions'

urlpatterns = [
    path('generate-predictions/', views.generate_predictions, name='generate_predictions'),
    path('api/predictions/', views.get_predictions_api, name='get_predictions_api'),
    path('patient/<int:patient_id>/predictions/', views.patient_prediction_detail, name='patient_prediction_detail'),
    path('medicine/<int:medicine_id>/predictions/', views.medicine_prediction_detail, name='medicine_prediction_detail'),
]