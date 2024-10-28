from django.urls import path
from . import views

app_name='patients'
urlpatterns = [
    path('', view=views.patient_list, name='patient_list'),
    # path('patients/', views.patient_list, name='patient_list'),
    path('create_patient/', view=views.create_patient, name='create_patient'),  # Create patient
    path('update/<int:patient_id>/', view=views.update_patient, name='update_patient'),  # Update patient
    path('delete/<int:patient_id>/', view=views.delete_patient, name='delete_patient'),  # Delete patient
]
