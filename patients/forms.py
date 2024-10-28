from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'contact_info']
    
    dob = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type':'date'}))
