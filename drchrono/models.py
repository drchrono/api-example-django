from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
import datetime as dt


# These models know very little about how they are created; only a bit of data that we want to cache locally, and how
# they're related to each other.

# TODO: They also aren't quite complete.
class Patient(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    social_security_number = models.CharField(null=True, max_length=255)

    def __str__(self):
        return "{self.first_name} {self.last_name}".format(self=self)


class Doctor(models.Model):
    first_name = models.CharField(max_length=255, editable=False)
    last_name = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return "Dr. {self.last_name}".format(self=self)


class AppointmentManager(models.Manager):
    def today(self):
        midnight = now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = midnight + dt.timedelta(days=1)
        return self.filter(
            scheduled_time__gte=midnight,
            scheduled_time__lte=tomorrow,
        ).order_by('scheduled_time')


class Appointment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)  # Appointments are keyed with a string, for better or worse
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)  # Breaks have a null patient field
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)  # Must have a doctor
    status = models.CharField(max_length=255, null=True)
    scheduled_time = models.DateTimeField(default=now, editable=False)
    duration = models.IntegerField(editable=False)
    checkin_time = models.DateTimeField(null=True)
    seen_time = models.DateTimeField(null=True)
    time_waiting = models.IntegerField(null=True)

    # custom manager with a today() method
    objects = AppointmentManager()

    def __str__(self):
        patient = self.patient or "Break"
        return "{self.scheduled_time} {patient} with {self.doctor} for {self.duration} minutes".format(
            self=self, patient=patient)
