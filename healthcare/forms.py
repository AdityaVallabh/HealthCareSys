from django.contrib.auth.models import User
from django import forms
from .models import Appointment
from django.forms.widgets import DateInput

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_time']
        widgets = {
            'appointment_time': forms.DateInput(attrs={
        'type':'date'})
        }
            
