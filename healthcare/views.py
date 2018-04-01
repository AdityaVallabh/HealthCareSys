from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, ProfileForm
from .models import UserProfile
from django.contrib.auth import logout

def index(request):
    return render(request, 'healthcare/home.html')

def logout_view(request):
    logout(request)
    return redirect('healthcare:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'healthcare/registration_form.html'

    def get(self, request):
        user_form = self.form_class(None)
        profile_form = ProfileForm(None)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            
            profile = ProfileForm(request.POST).save(commit=False)
            profile.user = user
            profile.save()
            
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('healthcare:index')

        return render(request, self.template_name, {'form': form})

