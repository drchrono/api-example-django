from django import forms
from django.conf import settings
#from localflavor.us.forms import USSocialSecurityNumberField

MAX_NAME_LENGTH = settings.MAX_NAME_LENGTH

class PatientForm(forms.Form):
    first_name = forms.CharField(label='Your first name', max_length=MAX_NAME_LENGTH)
    last_name = forms.CharField(label='Your last name', max_length=MAX_NAME_LENGTH)
    #ssn = USSocialSecurityNumberField()

