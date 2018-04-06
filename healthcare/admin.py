from django.contrib import admin
from .models import Hospital, Appointment


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact', 'email')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'user', 'doctor', 'appointment_time', 'status', 'fee')

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Appointment, AppointmentAdmin)