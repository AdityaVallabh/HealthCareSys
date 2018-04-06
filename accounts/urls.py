from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^home/$', views.UserFormView.as_view(), name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
