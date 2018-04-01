from django.conf.urls import url
from . import views

app_name = 'healthcare'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout_view, name='logout')
]
