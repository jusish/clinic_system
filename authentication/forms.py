from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor


class DoctorSignupForm(UserCreationForm):
    
    class Meta:
        model = Doctor
        fields = ('username', 'email','password1', 'password2', 'specialization')
        
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         Doctor.objects.create(user=user, specialization=self.cleaned_data['specialization'])
    #     return user