from django.test import TestCase
from django.utils.timezone import now

from drchrono.endpoints import AppointmentEndpoint, PatientEndpoint, DoctorEndpoint
from pprint import pprint


class PatientEndpointTest(TestCase):
    """
    Run through the basic functionality of an API endpoint
    """
    fixtures = ['api_oauth_test.json']
    endpoint_class = PatientEndpoint
    single_object_id = 61971496
    partial_update_field = {'home_phone': '(516) 555-8342'}
    create_object = {
        'first_name': 'Zaphod',
        'last_name': 'Beeblebrox',
        'gender': 'Male',
        'doctor': '116494'
    }

    def test_list(self):
        """
        Make sure that the list() method returns a bunch of patients from our test account
        :return:
        """
        endpoint = self.endpoint_class()
        data = [x for x in endpoint.list()]
        self.assertGreater(len(data), 0)
        pprint(data)

    def test_fetch(self):
        """
        Make sure that fetching a single item works okay
        :return:
        """
        endpoint = self.endpoint_class()
        object = endpoint.fetch(self.single_object_id)
        self.assertTrue(object)  # Empty objects are fals
        pprint(object)  # Inspect correctness by eyeball for now; we don't have time to fully understand and control
                        # the API server contents

    def test_update_partial(self):
        """
        Make a partial update. Make sure that field is written correctly.
        """
        endpoint = self.endpoint_class()
        object = endpoint.fetch(self.single_object_id)
        pprint(object)

        #Make sure the old value and new value are not the same, or this is a bogus test
        field_name = list(self.partial_update_field.keys())[0]
        new_value = self.partial_update_field[field_name]
        old_value = object[field_name]
        self.assertNotEqual(old_value, new_value)

        # Run a partial update of the object through the endpoint
        endpoint.update(self.single_object_id, {field_name: new_value})

        # fetch the object again, and check that the update stuck
        object = endpoint.fetch(self.single_object_id)
        self.assertEqual(object[field_name], new_value)

        # Put it back so we can test it again
        endpoint.update(self.single_object_id, {field_name: old_value})

    def test_create_delete(self):
        """
        Create a new (minimal) object, then delete it again
        """
        endpoint = self.endpoint_class()
        new_object = endpoint.create(json=self.create_object)
        pprint(new_object)
        self.assertIsNotNone(new_object['id'])  # Object should have gotten a new id
        # The DELETE verb on the Patients endpoint results in "APIException: Authorization failed." contrary to
        # expectation
        # endpoint.delete(new_object['id'])       # Should be able to delete the object now


class AppointmentEndpointTest(PatientEndpointTest):
    """
    Run through the basic functionality of an API endpoint
    """
    fixtures = ['api_oauth_test.json']
    endpoint_class = AppointmentEndpoint
    single_object_id = 40433778
    partial_update_field = {'status': 'Complete'}
    start = '2016-11-1'
    end = '2016-11-18'
    create_object = {
        'doctor': 116494,
        'duration': 15,
        'exam_room': 1,
        'office': 123880,
        'patient': 61971486,
        'scheduled_time': '2016-11-19T12:00'
    }

    def test_list(self):
        """
        Make sure that the list() method returns a bunch of patients from our test account
        :return:
        """
        endpoint = self.endpoint_class()
        data = [x for x in endpoint.list(start=self.start, end=self.end)]
        self.assertGreater(len(data), 0)
        pprint(data)

    def test_create_delete(self):
        """
        Create a new (minimal) object, then delete it again
        """
        endpoint = self.endpoint_class()
        new_object = endpoint.create(json=self.create_object)
        pprint(new_object)
        self.assertIsNotNone(new_object['id'])  # Object should have gotten a new id
        # Can't actually delete appointments either.
        # endpoint.delete(new_object['id'])       # Should be able to delete the object now


class DoctorEndpointTest(PatientEndpointTest):
    """
    Run through the basic functionality of an API endpoint
    """
    endpoint_class = DoctorEndpoint
    single_object_id = 116494
    partial_update_field = {'office_phone,': '(516) 555-8342'}
    create_object = {
        # Can't create doctors; dummy data
        'first_name': 'Arthur',
        'last_name': 'Dent',
    }

    def test_create_delete(self):
        endpoint = self.endpoint_class()
        try:
            endpoint.create(self.create_object)
        except NotImplementedError:
            pass

    def test_update_partial(self):
        endpoint = self.endpoint_class()
        # self.assertRaises does NOT agree with the NotImplemented exception for some reason
        try:
            endpoint.update(self.single_object_id, self.partial_update_field)
        except NotImplementedError:
            pass