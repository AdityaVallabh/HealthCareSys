from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime 
from accounts.models import DoctorProfile

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, default='123456789')
    email = models.CharField(max_length=100,default='hospital_email@gmail.com')

    def __str__(self):
        return self.name

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(default=datetime.now)
    appointment_time = models.DateTimeField()
    prescription = models.TextField(default='Prescription will be filled by the doctor.')
    status = models.CharField(max_length=500)
    fee = models.IntegerField(default=500)

    def __str__(self):
        return str(self.appointment_id) + ': ' + self.user.username + ' - ' + self.doctor.user.username
