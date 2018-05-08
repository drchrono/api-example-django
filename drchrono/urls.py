from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

import views


urlpatterns = [
    url(r'^setup/$', TemplateView.as_view(template_name='kiosk_setup.html'), name='setup'),
    url(r'^sync/$', views.sync_info, name='sync'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^check-in/$', views.PatientCheckin.as_view(), name='check-in'),
    url(r'^check-in/(?P<patient>\d+)/patient-info/$', views.PatientConfirmInfo.as_view(), name='confirm_info'),
    url(r'^check-in/(?P<patient>\d+)/appointments/$', views.PatientConfirmAppointment.as_view(), name='confirm_appointment'),
    url(r'^check-in/(?P<patient>\d+)/confirmed$', views.CheckinSuccess.as_view(), name='checkin_success'),
    url(r'^check-in/receptionist', views.CheckinFailed.as_view(), name='checkin_receptionist'),
    url(r'^today/$', login_required(views.DoctorToday.as_view(), login_url='setup'), name='today'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]