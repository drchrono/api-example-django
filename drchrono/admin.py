from django.contrib import admin

from drchrono.models import Patient, Appointment, Doctor


class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'date_of_birth', 'social_security_number']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']


class AppointmentAdmin(admin.ModelAdmin):
    """
    Primary admin interface to view *all* appointments.
    """
    list_display = ['patient', 'status', 'scheduled_time', 'checkin_time', 'time_waiting']


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
