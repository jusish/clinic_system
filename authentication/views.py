from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from billing.models import BillingRecord
from inventory.models import Medicine
from medical_records.models import MedicalRecord
from patients.models import Patient
from .forms import DoctorSignupForm
from datetime import datetime, timedelta

# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect('patients:patient_list')
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patients:patient_list')
    else:
        form = DoctorSignupForm()
    return render(request, 'authentication/signup.html', {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('patients:patient_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('patients:patient_list')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})
    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'authentication/logout_confirmation.html')




@login_required
def dashboard(request):
    # Fetching data from different apps
    total_patients = Patient.objects.count()
    total_billing_records = BillingRecord.objects.count()
    total_medicines = Medicine.objects.count()
    total_medical_records = MedicalRecord.objects.count()
    
    
    today = datetime.now()
    days = [(today - timedelta(days=i)).date() for i in range(7)]
    treated_patients = []
    for day in days:
        count = MedicalRecord.objects.filter(date=day).count()
        treated_patients.append(count)



    # Passing data to the template
    context = {
        'total_patients': total_patients,
        'total_billing_records': total_billing_records,
        'total_medicines': total_medicines,
        'total_medical_records': total_medical_records,
        'patients_labels': [day.strftime('%A') for day in days][::-1],  # Labels for chart (last 7 days)
        'patients_data': treated_patients[::-1],  # Reverse for chronological order
    }
    return render(request, 'authentication/dashboard.html', context)
