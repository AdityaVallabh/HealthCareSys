from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=500, blank=True)
    birth_date = models.DateField(blank=True)

    def __str__(self):
        return self.user.username

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    contact = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username