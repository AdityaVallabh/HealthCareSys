from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'healthcare'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^appointment/$', views.AppointmentCreate.as_view(), name='book-appointment'),
    url(r'^appointment/(?P<pk>[0-9]+)/', views.AppointmentDetail.as_view(), name='appointment-detail'),
    url(r'^edit-appointment/(?P<pk>[0-9]+)/$', views.AppointmentUpdate.as_view(), name='appointment-update'),
    url(r'^transactions/$', views.TransactionListView.as_view(), name='transactions'),
    url(r'^transaction/(?P<pk>[0-9]+)/', views.TransactionDetail.as_view(), name='transaction-detail'),
    url(r'^search/', views.search, name='search'),
    url(r'^print/', views.print_report, name='print'),
]
