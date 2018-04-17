from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^updateuser/$', views.UserFormUpdate.as_view(), name='userupdate'),
    #url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^user/(?P<pk>[0-9]+)/', views.UserDetail.as_view(), name='user-detail'),
    url(r'^doctor/(?P<pk>[0-9]+)/', views.DoctorDetail.as_view(), name='doctor-detail'),
    url(r'^home/$', views.UserFormView.as_view(), name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
