from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views

import views


urlpatterns = [
    url(r'^$', views.home , name='home'),
    url(r'^your-patient/$', views.patient_signin, name='patient'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'login/$', auth_views.login, name='login'),
]
