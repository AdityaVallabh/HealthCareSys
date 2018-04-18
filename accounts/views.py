from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, ProfileForm, DoctorForm, UpdateUserProfile
from .models import UserProfile, DoctorProfile ,User
from django.contrib.auth import logout
from healthcare.models import Department
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        if request.GET.get('role', 'user') == 'doctor':
            profile_form = DoctorForm(None)
        else:
            profile_form = ProfileForm(None)

        user_form = self.form_class(None)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    @transaction.atomic
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            if request.GET.get('role', 'user') == 'doctor':
                profile = DoctorForm(request.POST).save(commit=False)
                Department.objects.get_or_create(department_name=profile.specialization)
            else:
                profile = ProfileForm(request.POST).save(commit=False)
            profile.user = user
            profile.save()
            
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('healthcare:index')

        return render(request, self.template_name, {'form': form, 'message': form.errors})
class UserDetail(generic.DetailView):
    model = UserProfile
    template_name = 'registration/userprofile.html'

class DoctorDetail(generic.DetailView):
    model = DoctorProfile
    template_name = 'registration/doctorprofile.html'

@method_decorator(login_required, name='dispatch')
class UserFormUpdate(View):
    template_name = 'registration/userupdate.html'
    form_class = UpdateUserProfile
    def get(self, request):
        if hasattr(request.user,'doctorprofile'):
            profile_form = DoctorForm(initial={'contact':request.user.doctorprofile.contact,'hospital':request.user.doctorprofile.hospital,'specialization':request.user.doctorprofile.specialization,'consultation_fee':request.user.doctorprofile.consultation_fee})
        elif hasattr(request.user,'userprofile'):
            profile_form = ProfileForm(initial={'contact':request.user.userprofile.contact,'address':request.user.userprofile.address,'birth_date':request.user.userprofile.birth_date})
            
        user_form = self.form_class(initial={'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        queryset = User.objects.filter(id=request.user.id).first()
        form = self.form_class(request.POST, instance=queryset)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            username = request.user
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            if request.GET.get('role', 'user') == 'doctor':
                query = DoctorProfile.objects.filter(id=request.user.doctorprofile.id).first()
                profile = DoctorForm(request.POST).save(commit=False)
                Department.objects.get_or_create(department_name=profile.specialization)
            else:
                query = UserProfile.objects.filter(id=request.user.userprofile.id).first()
                profile = ProfileForm(request.POST, instance=query).save(commit=False)
            profile.user = request.user
            profile.save()
            
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('healthcare:index')

        return render(request, self.template_name, {'form': form, 'message': form.errors})

