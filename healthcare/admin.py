from django.contrib import admin
from .models import UserProfile, DoctorProfile, Hospital

admin.site.register(UserProfile)
admin.site.register(DoctorProfile)
admin.site.register(Hospital)
