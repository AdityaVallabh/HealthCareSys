from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime 
from accounts.models import DoctorProfile
from django.core.urlresolvers import reverse
from django.db import transaction

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=500)

    def __str__(self):
        return self.location_name

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location)
    contact = models.CharField(max_length=100, default='123456789')
    email = models.CharField(max_length=100,default='hospital_email@gmail.com')
    amount = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=500)

    def __str__(self):
        return self.department_name

class Transaction(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    time = models.DateTimeField(default=datetime.now)
    amount = models.PositiveIntegerField()
    reason = models.CharField(max_length=100)
    success = models.BooleanField(default=False)

    @transaction.atomic
    def make_transaction(self,from_user, to_user, amount, reason):
        status = False
        if from_user.amount >= amount:
            from_user.amount -= amount
            to_user.amount += amount
            from_user.save()
            to_user.save()
            status = True
        transaction = Transaction(from_user=from_user.user, to_user=to_user.user, amount=amount, success=status, reason=reason)
        transaction.save()
        return transaction, status

    def get_absolute_url(self):
        return reverse('healthcare:transaction-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id) + ': ' + str(self.from_user) + ' to ' + str(self.to_user) + ' - ' + str(self.amount)



class Appointment(models.Model):
    STATUS = (
        ('Unconfirmed', 'Unconfirmed'),
        ('Confirmed', 'Confirmed'),
    )
    appointment_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction)
    user = models.ForeignKey(User)
    doctor = models.ForeignKey(DoctorProfile)
    booking_time = models.DateTimeField(default=datetime.now)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(blank=True, null=True)
    prescription = models.TextField(default='Prescription will be filled by the doctor.')
    status = models.CharField(max_length=20, default='Unconfirmed', choices=STATUS)
    fee = models.PositiveIntegerField(default=500)

    def get_absolute_url(self):
        return reverse('healthcare:appointment-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.appointment_id) + ': ' + self.user.username + ' - ' + self.doctor.user.username


        
