import requests
from social.apps.django_app.default.models import UserSocialAuth
import logging


class APIException(Exception): pass


class Forbidden(APIException): pass


class NotFound(APIException): pass


class Conflict(APIException): pass


ERROR_CODES = {
    403: Forbidden,
    404: NotFound,
    409: Conflict,
}


# TODO: this API abstraction is included for your convenience. If you don't like it, feel free to change it.
class BaseEndpoint(object):
    """
    A python wrapper for the basic rules of the drchrono API endpoints.

    Provides consistent, pythonic usage and return values from the API.

    Abstracts away:
     - base URL,
     - details of authentication
     - list iteration
     - response codes

    All return values will be dicts, or lists of dicts.

    Subclasses should implement a specific endpoint.
    """
    BASE_URL = 'https://drchrono.com/api/'
    endpoint = ''

    def __init__(self):
        """
        Creates an API client which will act on behalf of a specific user
        """
        self.oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        self.access_token = self.oauth_provider.extra_data['access_token']

    @property
    def logger(self):
        name = "{}.{}".format(__name__, self.endpoint)
        return logging.getLogger(name)

    def _url(self, id=""):
        if id:
            id = "/{}".format(id)
        return "{}{}{}".format(self.BASE_URL, self.endpoint, id)

    def _auth_headers(self, kwargs):
        """
        Adds auth information to the kwargs['header'], as expected by get/put/post/delete

        Modifies kwargs in place. Returns None.
        """
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update({
            'Authorization': 'Bearer {}'.format(self.access_token),

        })

    def _json_or_exception(self, response):
        """
        returns the JSON content or raises an exception, based on what kind of response (2XX/4XX) we get
        """
        if response.ok:
            if response.status_code != 204: # No Content
                return response.json()
        else:
            exe = ERROR_CODES.get(response.status_code, APIException)
            raise exe(response.content)

    def _request(self, method, *args, **kwargs):
        # dirty, universal way to use the requests library directly for debugging
        url = self._url(kwargs.pop(id, ''))
        self._auth_headers(kwargs)
        return getattr(requests, method)(url, *args, **kwargs)

    def list(self, params=None, **kwargs):
        """
        Returns an iterator to retrieve all objects at the specified resource. Waits to exhaust the current page before
        retrieving the next, which might result in choppy responses.
        """
        self.logger.debug("list()")
        url = self._url()
        self._auth_headers(kwargs)
        # Response will be one page out of a paginated results list
        response = requests.get(url, params=params, **kwargs)
        if response.ok:
            self.logger.debug("list got page {}".format('url'))
            while url:
                data = response.json()
                url = data['next']  # Same as the resource URL, but with the page query parameter present
                for result in data['results']:
                    yield result
        else:
            exe = ERROR_CODES.get(response.status_code, APIException)
            self.logger.debug("list exception {}".format(exe))
            raise exe(response.content)
        self.logger.debug("list() complete")

    def fetch(self, id, params=None, **kwargs):
        """
        Retrieve a specific object by ID
        """
        url = self._url(id)
        self._auth_headers(kwargs)
        response = requests.get(url, params=params, **kwargs)
        self.logger.info("fetch {}".format(response.status_code))
        return self._json_or_exception(response)

    def create(self, data=None, json=None, **kwargs):
        """
        Used to create an object at a resource with the included values.

        Response body will be the requested object, with the ID it was assigned.

        Success: 201 (Created)
        Failure:
           - 400 (Bad Request)
           - 403 (Forbidden)
           - 409 (Conflict)
        """
        url = self._url()
        self._auth_headers(kwargs)
        response = requests.post(url, data=data, json=json, **kwargs)
        return self._json_or_exception(response)

    def update(self, id, data, partial=True, **kwargs):
        """
        Updates an object. Returns None.

        When partial=False, uses PUT to update the entire object at the given ID with the given values.

        When partial=TRUE [the default] uses PATCH to update only the given fields on the object.

        Response body will be empty.

        Success: 204 (No Content)
        Failure:
           - 400 (Bad Request)
           - 403 (Forbidden)
           - 409 (Conflict)
        """
        url = self._url(id)
        self._auth_headers(kwargs)
        if partial:
            response = requests.patch(url, data, **kwargs)
        else:
            response = requests.put(url, data, **kwargs)
        return self._json_or_exception(response)

    def delete(self, id, **kwargs):
        """
        Deletes the object at this resource with the given ID.

        Response body will be empty.

        Success: 204 (No Content)
        Failure:
           - 400 (Bad Request)
           - 403 (Forbidden)
        """
        url = self._url(id)
        self._auth_headers(kwargs)
        response = requests.delete(url)
        return self._json_or_exception(response)


class PatientEndpoint(BaseEndpoint):
    endpoint = "patients"


class AppointmentEndpoint(BaseEndpoint):
    endpoint = "appointments"

    # Special parameter requirements for a given resource should be explicitly called out
    def list(self, params=None, date=None, start=None, end=None, **kwargs):
        """
        List appointments on a given date, or between two dates
        """
        # Just parameter parsing & checking
        params = params or {}
        if start and end:
            date_range = "{}/{}".format(start, end)
            params['date_range'] = date_range
        elif date:
            params['date'] = date
        if 'date' not in params and 'date_range' not in params:
            raise Exception("Must provide either start & end, or date argument")
        return super(AppointmentEndpoint, self).list(params, **kwargs)


class DoctorEndpoint(BaseEndpoint):
    endpoint = "doctors"

    def update(self, id, data, partial=True, **kwargs):
        raise NotImplementedError("the API does not allow updating doctors")

    def create(self, data=None, json=None, **kwargs):
        raise NotImplementedError("the API does not allow creating doctors")

    def delete(self, id, **kwargs):
        raise NotImplementedError("the API does not allow deleteing doctors")


class AppointmentProfileEndpoint(BaseEndpoint):
    endpoint = "appointment_profiles"
