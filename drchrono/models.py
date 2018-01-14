from django.db import models
from django.conf import settings

from datetime import date
#from localflavor.us.forms import USSocialSecurityNumberField

MAX_NAME_LENGTH = settings.MAX_NAME_LENGTH

# Create your models here.
class Doctor(models.Model):
  doctor_id = models.AutoField(primary_key=True)
  last_name = models.CharField(max_length=MAX_NAME_LENGTH)
  first_name = models.CharField(max_length=MAX_NAME_LENGTH)

class Patient(models.Model):
  date_lastupdated = models.DateField(auto_now=True)
  last_name = models.CharField(max_length=MAX_NAME_LENGTH)
  first_name = models.CharField(max_length=MAX_NAME_LENGTH)
  dob = models.DateField()
  doctor = models.ForeignKey(Doctor)
  patient_id = models.AutoField(primary_key=True)
  #ssn = USSocialSecurityNumberField()
  
class Appointment(models.Model):
  date_of_appointment = models.DateField(auto_now=False)

