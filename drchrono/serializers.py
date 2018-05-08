from rest_framework.serializers import ModelSerializer
from drchrono.models import Doctor, Patient, Appointment
from django.utils import timezone
import datetime as dt


class LimitedModelSerializer(ModelSerializer):
    """
    These serializer classes are designed to pull data out of the API and into the local Database
    """

    def to_representation(self, instance):
        """
        raises NotImplemented. This app does NOT push models outbound; any editing required is done directly through
        the API.
        """
        raise NotImplemented("This is a one-way serializer; API -> Model only")

    def to_internal_value(self, data):
        """
        Discards all data that isn't specified in self.fields, since we don't care to store it.
        """
        internal_data = {k: data[k] for k in self.fields}
        for k in list(internal_data.keys()):
            # the API gives us naive datetimes; assume they are in the local time of this kiosk.
            # Side note: this is a pretty big design problem for the API system now, without an easy fix.
            if isinstance(internal_data[k], dt.datetime) and internal_data[k].tzinfo is None:
                dt_aware = timezone.make_aware(internal_data[k], timezone.get_current_timezone())
                internal_data[k] = dt_aware
        return internal_data


class PatientSerializer(LimitedModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'date_of_birth')
        depth = 1


class DoctorSerializer(LimitedModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name')
        depth = 1


class AppointmentSerializer(LimitedModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'doctor', 'status', 'scheduled_time', 'duration')
        depth = 1

    # We push the update/create responsibility to the API resource layer so the serializers don't need to know how to
    # connect to the API at all; instead they just handle the data
    def create(self, validated_data):
        """
        Only allows appointment creation if the referenced Doctor and Patient are already in the database

        Raises Doctor.DoesNotExist or Patient.DoesNotExist when they aren't.
        """
        doctor_id = validated_data.pop('doctor')
        validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
        patient_id = validated_data.pop('patient')
        validated_data['patient'] = Patient.objects.get(id=patient_id)
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Only allows appointment updates if the referenced Doctor and Patient are already in the database.

        Raises Doctor.DoesNotExist or Patient.DoesNotExist when they aren't.
        """
        doctor_id = validated_data.pop('doctor')
        validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
        patient_id = validated_data.pop('patient')
        validated_data['patient'] = Patient.objects.get(id=patient_id)
        # Only works because the model is so simple.
        for field_name in self.fields:
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance

    def save(self, **kwargs):
        # Dirty hack to ensure that save() will update instances if they exist
        try:
            id = self.validated_data['id']
            model = self.__class__.Meta.model
            self.instance = model.objects.get(id=id)
        except self.Meta.model.DoesNotExist:
            pass
        super(AppointmentSerializer, self).save(**kwargs)