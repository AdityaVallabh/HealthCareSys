from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Hospital
from accounts.models import DoctorProfile

def index(request):
    if not request.GET.get('location', 'none') == 'none' and not request.GET.get('specialty', 'none') == 'none':
        location = request.GET['location']
        specialty = request.GET['specialty']
        hospitals = Hospital.objects.filter(location__contains=location)
        doctors = []
        for hospital in hospitals:
            doctors += DoctorProfile.objects.filter(hospital=hospital, specialization__contains=specialty)
        return render(request, 'healthcare/home.html', {'doctors': doctors})    
    return render(request, 'healthcare/home.html')



