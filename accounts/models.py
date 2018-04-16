from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=500, blank=True)
    birth_date = models.DateField(blank=True)
    amount = models.PositiveIntegerField(default=1500)

    def get_absolute_url(self):
        return reverse('account:user', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey('healthcare.Hospital', on_delete=models.CASCADE)
    contact = models.CharField(max_length=50)
    specialization = models.ForeignKey('healthcare.Department', on_delete=models.CASCADE)
    consultation_fee = models.IntegerField(default=200)
    amount = models.PositiveIntegerField(default=100)

    def get_absolute_url(self):
        return reverse('account:user', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username
