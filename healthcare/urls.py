from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'healthcare'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^appointment/', views.AppointmentCreate.as_view(), name='book-appointment'),
    url(r'^(?P<pk>[0-9]+)/', views.AppointmentDetail.as_view(), name='appointment-detail'),
    url(r'^search/', views.search, name='search'),
]
