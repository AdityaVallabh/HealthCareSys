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
from datetime import datetime
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .resources import AppointmentResource, TransactionResource

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

def print_report(request):
    if request.user.is_superuser:
        if request.GET.get('data', 'none') == 'appointments':
            appointment_resource = AppointmentResource()
            dataset = appointment_resource.export()
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="appointments.csv"'
            return response
        elif request.GET.get('data', 'none') == 'transactions':
            transaction_resource = TransactionResource()
            dataset = transaction_resource.export()
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
            return response
    return redirect('/')
            

def export(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response

@method_decorator(login_required, name='dispatch')
class AppointmentCreate(CreateView):
    form_class = AppointmentForm
    template_name = 'healthcare/appointment_form.html'
    doctor = None

    def send_email(self, transaction):
        try:
            subject = "Invoice for Transaction %d" % transaction.id
            body = """
Greetings %s %s!
You've recently carried out a transaction on HealthCareSys. Here are the details for future reference:-

Transaction ID: %d
From: %s
To: %s
Amount: %d
DateTime: %s
Success: %s

Wishing you the best of health,
Team HealthCareSys.
""" % (transaction.from_user.first_name, transaction.from_user.last_name, transaction.id, transaction.from_user.username, transaction.to_user.username, transaction.amount, transaction.time, transaction.success)
            email = EmailMessage(subject, body, to=[transaction.from_user.email])
            email.send()
        except:
            print("Unable to send email (%s)" % transaction.from_user.email)
    def get_initial(self):
        if self.request.GET.get('doctor_id') and DoctorProfile.objects.filter(id=self.request.GET['doctor_id']):
            return { 'doctor': DoctorProfile.objects.get(id=self.request.GET['doctor_id'])}
    
    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.user = self.request.user
        appointment.fee = appointment.doctor.consultation_fee
        
        transaction = Transaction()
        transaction, success = transaction.make_transaction(from_user=self.request.user.userprofile, to_user=appointment.doctor, amount=appointment.fee, reason="Book Appointment")
        if success:
            appointment.transaction_id = transaction
            appointment.save()
        else:
            print('Transaction %d failed' % transaction.id)
        self.send_email(transaction)
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
        return super(AppointmentUpdate,self).dispatch(request, *args, **kwargs)

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
            
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)   
         
        appointments=[]
        past_appointments =[]

        upcoming_appointments = []

        if hasattr(self.request.user, 'userprofile'):
            appointments=Appointment.objects.filter(user=self.request.user)
        elif hasattr(self.request.user, 'doctorprofile'):
            appointments=Appointment.objects.filter(doctor=self.request.user.doctorprofile)
        elif (self.request.user.is_superuser):
            appointments = Appointment.objects.all()

        for appointment in appointments:
            x=datetime.combine(appointment.appointment_date,datetime.min.time())
            z=datetime.now()
            if  x < z:
                past_appointments += [appointment]
            else:
                upcoming_appointments += [appointment]
        
        context['past_appointments'] = past_appointments
        
        context['upcoming_appointments'] = upcoming_appointments
        
        return context


class AppointmentDetail(generic.DetailView):
    model = Appointment
    template_name = 'healthcare/appointment.html'

class TransactionListView(generic.ListView):
    template_name = 'healthcare/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        elif self.request.user.is_authenticated():
            return Transaction.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))

class TransactionDetail(generic.DetailView):
    model = Transaction
    template_name = 'healthcare/transaction-detail.html'
