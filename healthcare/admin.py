from django.contrib import admin
from .models import Hospital, Appointment, Department, Location, Transaction


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact', 'email')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'user', 'doctor', 'appointment_time', 'status', 'fee')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'location_name')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'amount', 'success')

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Transaction, TransactionAdmin)