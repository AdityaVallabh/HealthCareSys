from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'healthcare'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
