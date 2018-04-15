from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Hospital, Appointment, Location, Department, Transaction
from accounts.models import DoctorProfile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.widgets import DateInput
from .forms import AppointmentForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

def index(request):
    return render(request, 'healthcare/home.html')

def search(request):
    locations = Location.objects.all().order_by('location_name')
    departments = Department.objects.all().order_by('department_name')
    if not request.GET.get('location', 'none') == 'none' and not request.GET.get('specialty', 'none') == 'none':
        location = request.GET['location']
        specialty = request.GET['specialty']
        location = Location.objects.filter(location_name=location)
        hospitals = Hospital.objects.filter(location=location)
        doctors = []
        for hospital in hospitals:
            specialty = Department.objects.filter(department_name=specialty)
            doctors += DoctorProfile.objects.filter(hospital=hospital, specialization=specialty)

        return render(request, 'healthcare/search.html', {'doctors': doctors, 'locations': locations, 'departments': departments})

    return render(request, 'healthcare/search.html', {'locations': locations, 'departments': departments})


@method_decorator(login_required, name='dispatch')
class AppointmentCreate(CreateView):
    form_class = AppointmentForm
    template_name = 'healthcare/appointment_form.html'
    doctor = None

    def get_initial(self):
        if self.request.GET.get('doctor_id') and DoctorProfile.objects.filter(id=self.request.GET['doctor_id']):
            return { 'doctor': DoctorProfile.objects.get(id=self.request.GET['doctor_id'])}
    
    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.user = self.request.user
        appointment.fee = appointment.doctor.consultation_fee
        transaction, success = Transaction.make_transaction(from_user=self.request.user.userprofile, to_user=appointment.doctor, amount=appointment.fee, reason="Book Appointment")
        if success:
            appointment.transaction_id = transaction
            appointment.save()
        else:
            print('Transaction %d failed' % transaction.id)
        return redirect('healthcare:index')

@method_decorator(login_required, name='dispatch')
class AppointmentUpdate(UpdateView):
    model = Appointment
    template_name = 'healthcare/appointment_update.html'        

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'doctorprofile'):
            self.fields = ['appointment_time', 'status', 'prescription']
        else:
            self.fields = ['appointment_date']
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        appointment = form.save(commit=False)
        if hasattr(self.request.user, 'userprofile'):
            appointment.status = 'Unconfirmed'
            appointment.appointment_time = None
        appointment.save() 
        return redirect(self.get_success_url())

    
    
class IndexView(generic.ListView):
    template_name = 'healthcare/home.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            if hasattr(self.request.user, 'userprofile'):
                return Appointment.objects.filter(user=self.request.user)
            elif hasattr(self.request.user, 'doctorprofile'):
                return Appointment.objects.filter(doctor=self.request.user.doctorprofile)

class AppointmentDetail(generic.DetailView):
    model = Appointment
    template_name = 'healthcare/appointment.html'

class TransactionListView(generic.ListView):
    template_name = 'healthcare/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Transaction.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))

class TransactionDetail(generic.DetailView):
    model = Transaction
    template_name = 'healthcare/transaction-detail.html'