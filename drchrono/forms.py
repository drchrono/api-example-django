from django import forms
from django.forms import widgets

from drchrono.models import Patient, Appointment, Doctor


class PatientWhoamiForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=widgets.DateInput)
    social_security_number = forms.CharField(required=False)

    # TODO: form validation

    def get_patient(self):
        data = {f: self.cleaned_data[f] for f in self.cleaned_data if self.cleaned_data[f]}
        # All form fields should be patient attributes, so we can construct filters this cheezy way.
        filters = {"{}".format(f): data[f] for f in data}
        return Patient.objects.get(**filters)


class PatientInfoForm(forms.Form):
    pass
    # TODO: finish this

# TODO: Bonus Challenge! custom demographics fields are dynamically constructed; this is tricky with django forms.


class AppointmentChoiceForm(forms.Form):
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        widget=widgets.RadioSelect,
        empty_label=None,
    )

