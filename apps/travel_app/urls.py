from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index, name = 'main_page'),
    url(r'^appointments$', views.dashboard, name = 'dashboard'),
    url(r'^travels/add$', views.add_appt, name = 'add_appt'),
    url(r'^main/login$', views.login, name = 'login'),
    url(r'^main/register$', views.register, name = 'register'),
    url(r'^appointments/(?P<id>\d+)$', views.edit_appt, name ='edit_appt'),
    url(r'^appointments/(?P<id>\d+)/delete$', views.delete, name= 'delete_appt'),
    url(r'^logout', views.logout, name = 'logout')
]
