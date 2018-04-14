from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, ProfileForm, DoctorForm
from .models import UserProfile, DoctorProfile ,User
from django.contrib.auth import logout
from healthcare.models import Department
from django.views import generic

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
