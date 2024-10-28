from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import DoctorSignupForm

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
