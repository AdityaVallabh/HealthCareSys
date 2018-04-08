from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Hospital, Appointment
from accounts.models import DoctorProfile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.widgets import DateInput
from .forms import AppointmentForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def search(request):
    if not request.GET.get('location', 'none') == 'none' and not request.GET.get('specialty', 'none') == 'none':
        location = request.GET['location']
        specialty = request.GET['specialty']
        hospitals = Hospital.objects.filter(location__contains=location)
        doctors = []
        for hospital in hospitals:
            doctors += DoctorProfile.objects.filter(hospital=hospital, specialization__contains=specialty)
        return render(request, 'healthcare/home.html', {'doctors': doctors})    
    return render(request, 'healthcare/home.html')


@method_decorator(login_required, name='dispatch')
class AppointmentCreate(CreateView):
    form_class = AppointmentForm
    template_name = 'healthcare/appointment_form.html'

    def get_initial(self):
        if self.request.GET.get('doctor_id') and DoctorProfile.objects.filter(id=self.request.GET['doctor_id']):
            return { 'doctor': DoctorProfile.objects.get(id=self.request.GET['doctor_id'])}
    
    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.user = self.request.user
        appointment.save()
        return redirect('healthcare:index')


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