from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, DoctorProfile
from django.forms.widgets import DateInput

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['contact', 'address', 'birth_date']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})
        }

class DoctorForm(forms.ModelForm):

    class Meta:
        model = DoctorProfile
        fields = ['hospital', 'contact', 'specialization']

