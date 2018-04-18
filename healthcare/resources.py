from import_export import resources
from .models import Appointment, Transaction

class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointment

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        