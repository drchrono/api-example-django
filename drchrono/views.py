from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.utils.timezone import now
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.db import models

from drchrono.endpoints import PatientEndpoint, AppointmentEndpoint
from drchrono.forms import PatientWhoamiForm, AppointmentChoiceForm, PatientInfoForm
from drchrono.models import Appointment, Patient
from drchrono.serializers import AppointmentSerializer
from drchrono.sync import sync_all

# These views are very basic; they use almost no JS, have very little interactivity, and probably aren't well designed.
# TODO: you have free reign in this module to discard anything and make it better.


#####
# Patient checkin flow
class PatientCheckin(generic.FormView):
    """
    The first view a patient sees when they come to the kiosk
    """
    form_class = PatientWhoamiForm
    template_name = 'form_patient_identify.html'

    def form_valid(self, form):
        try:
            patient = form.get_patient()
            return redirect('confirm_appointment', patient=patient.id)
        except Patient.DoesNotExist:
            return redirect('checkin_receptionist')


class PatientConfirmAppointment(generic.FormView):
    """
    The patient can select their appointment from a list.
    """
    form_class = AppointmentChoiceForm
    template_name = 'form_appointment_select.html'

    def get_form_kwargs(self):
        # TODO: fix this security hole:
        # By tampering with the GET parameter, a bad actor can retrieve a list  of all appointments for any patient.
        old_kwargs = super(PatientConfirmAppointment, self).get_form_kwargs()
        patient_id = self.kwargs['patient']
        old_kwargs.update({
            'patient': patient_id,
        })
        return old_kwargs

    def form_valid(self, form):
        # Hit the Appointments API and confirm check-in
        appointment = form.cleaned_data['appointment']
        endpoint = AppointmentEndpoint()
        endpoint.update(appointment.id, {'status': 'Arrived'})
        # Re-sync the appointment info to update the status, and pick up any other updates since last time
        api_data = endpoint.fetch(id=appointment.id)
        serializer = AppointmentSerializer(data=api_data)
        if serializer.is_valid():
            serializer.save()  # Save updates from API
            # Redirect for the next visitor to check in
            return redirect('checkin_success', patient=form.patient)
        else:
            # TODO: set up logging framework properly
            # logger.error("Error saving appointment {}".format(appointment.id))
            return redirect('checkin_receptionist')


class PatientConfirmInfo(generic.FormView):
    """
    The patient can edit their demographic data. The kiosk will use the API to update demographic info about the patient
    """
    # TODO: finish this. It does not work at all.
    template_name = 'form_patient_info.html'
    form_class = PatientInfoForm


class CheckinSuccess(generic.TemplateView):
    """
    Display a 'success' message when a patient has checked in.
    """
    template_name = 'checkin_success.html'


class CheckinFailed(TemplateView):
    """
    Display a 'failure' message and a call-to-action for the patient to see the IRL receptionist.
    """
    template_name = 'checkin_receptionist.html'


######
# Doctor dashboard
class DoctorToday(ListView):
    """
    The doctor can see what appointments they have today.
    """
    # TODO: this needs some work for the doctor to use it as a control panel for their daily schedule.
    template_name = 'doctor_today.html'
    queryset = Appointment.objects.all()

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorToday, self).get_context_data(**kwargs)
        kwargs['current_time'] = now()
        wait_time = Appointment.objects.filter(
            time_waiting__isnull=False
        ).aggregate(models.Avg('time_waiting'))['time_waiting__avg']
        kwargs['wait_time'] = wait_time
        return kwargs


###############
# Utility views
def sync_info(request):
    """Sync everything, then redirect back to the today screen"""
    sync_all()
    return redirect('today')
