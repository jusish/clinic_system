from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Count, Sum
import json

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
            return redirect('dashboard')
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
            return redirect('dashboard')
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
    # Basic stats
    total_patients = Patient.objects.count()
    total_billing_records = BillingRecord.objects.count()
    total_medicines = Medicine.objects.count()
    total_medical_records = MedicalRecord.objects.count()
    
    # Get last 7 days data for line chart
    today = timezone.now()
    days = [(today - timedelta(days=i)).date() for i in range(7)]
    treated_patients = []
    
    for day in days:
        count = MedicalRecord.objects.filter(date__date=day).count()
        treated_patients.append(count)

    # Monthly revenue data for bar chart (last 6 months)
    months = [(today - timedelta(days=30*i)) for i in range(6)]
    monthly_revenue = []
    month_labels = []
    
    for month in months:
        revenue = BillingRecord.objects.filter(
            date__year=month.year,
            date__month=month.month
        ).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        monthly_revenue.append(float(revenue))
        month_labels.append(month.strftime('%B %Y'))

    # Medicine inventory status for doughnut chart
    low_stock = Medicine.objects.filter(quantity__lt=10).count()
    adequate_stock = Medicine.objects.filter(quantity__gte=10, quantity__lt=50).count()
    high_stock = Medicine.objects.filter(quantity__gte=50).count()

    # Recent activity for timeline
    recent_records = MedicalRecord.objects.select_related('patient', 'doctor').order_by('-date')[:5]
    recent_activity = [{
        'type': 'medical_record',
        'patient': record.patient.name,
        'doctor': record.doctor.username,
        'date': record.date.strftime('%Y-%m-%d %H:%M'),
        'action': 'Medical consultation'
    } for record in recent_records]

    context = {
        'total_patients': total_patients,
        'total_billing_records': total_billing_records,
        'total_medicines': total_medicines,
        'total_medical_records': total_medical_records,
        
        # Line chart data
        'patients_data': json.dumps(treated_patients[::-1]),
        'patients_labels': json.dumps([day.strftime('%Y-%m-%d') for day in days][::-1]),
        
        # Bar chart data
        'monthly_revenue': json.dumps(monthly_revenue[::-1]),
        'month_labels': json.dumps(month_labels[::-1]),
        
        # Doughnut chart data
        'inventory_data': json.dumps([low_stock, adequate_stock, high_stock]),
        
        # Recent activity
        'recent_activity': recent_activity,
    }
    return render(request, 'authentication/dashboard.html', context)
