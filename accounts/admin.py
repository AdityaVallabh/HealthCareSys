from django.contrib import admin
from .models import UserProfile, DoctorProfile

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital', 'contact', 'specialization')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'address', 'birth_date')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
