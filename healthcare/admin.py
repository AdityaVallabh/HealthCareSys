from django.contrib import admin
from .models import UserProfile, DoctorProfile, Hospital, Appointment


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital', 'contact', 'specialization')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'address', 'birth_date')
    
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact', 'email')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'user', 'doctor', 'appointment_time', 'status', 'fee')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Appointment, AppointmentAdmin)