from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'healthcare'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
