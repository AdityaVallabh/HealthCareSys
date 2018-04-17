from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, DoctorProfile
from django.forms.widgets import DateInput

class UserForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control','id':'search-bar','required':''}))
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control','id':'search-bar','required':''}))
    email = forms.EmailField(label='email',widget=forms.TextInput(attrs={'type':'email','placeholder':'Email','class':'form-control','id':'search-bar','required':''}))
    first_name = forms.CharField(label='first_name',widget=forms.TextInput(attrs={'placeholder':'First Name','class':'form-control','id':'search-bar','required':''}))
    last_name = forms.CharField(label='last_name',widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'form-control','id':'search-bar','required':''}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    contact = forms.CharField(label='contact',widget=forms.TextInput(attrs={'placeholder':'Contact','class':'form-control','id':'search-bar','required':''}))
    address = forms.CharField(label='address',widget=forms.TextInput(attrs={'placeholder':'Address','class':'form-control','id':'search-bar'}))
    birth_date = forms.DateField(label='Date',widget=forms.TextInput(attrs={'type': 'date','placeholder':'Date Of Birth','class':'form-control','id':'search-bar'}))
    class Meta:
        model = UserProfile
        fields = ['contact', 'address', 'birth_date']


class DoctorForm(forms.ModelForm):
    #hospital = forms.CharField(label='hospital',widget=forms.Select(attrs={'placeholder':'Hospital','class':'form-control','id':'search-bar','required':''}))
    #hospital = forms.CharField(label='hospital',widget=forms.ForeignKeyWidget(hospital_id,'name',attrs={'placeholder':'Hospital','class':'form-control','id':'search-bar','required':''}))
    contact = forms.CharField(label='contact',widget=forms.TextInput(attrs={'placeholder':'Contact','class':'form-control','id':'search-bar','required':''}))
    specialization = forms.CharField(label='specialization',widget=forms.TextInput(attrs={'placeholder':'Specialization','class':'form-control','id':'search-bar','required':''}))
    consultation_fee = forms.IntegerField(label='consultation_fee',widget=forms.TextInput(attrs={'placeholder':'Consultation Fee','class':'form-control','id':'search-bar','required':''}))
    class Meta:
        model = DoctorProfile
        fields = ['hospital', 'contact', 'specialization','consultation_fee']
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control','id':'search-bar','placeholder':'Hospital','required':''}),
        }

class UpdateUserProfile(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control','id':'search-bar','required':''}))
    #username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control','id':'search-bar','required':''}))
    email = forms.EmailField(label='email',widget=forms.TextInput(attrs={'type':'email','placeholder':'Email','class':'form-control','id':'search-bar','required':''}))
    first_name = forms.CharField(label='first_name',widget=forms.TextInput(attrs={'placeholder':'First Name','class':'form-control','id':'search-bar','required':''}))
    last_name = forms.CharField(label='last_name',widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'form-control','id':'search-bar','required':''}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password']


