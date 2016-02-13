from requests.models import complexjson
from functools import wraps
import hashlib
import json
import requests


class DeserializeError(Exception):

    pass


class ApiError(Exception):

    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

    def __str__(self):
        return '%d: %s' % (self.status_code, self.reason)


class ApiResponse(object):

    error_messages = {
        # method exceptions
        400: 'General api method exception',
        420: 'Validation error',
        # general api exceptions
        500: 'General api exception',
        514: 'Invalid module',
        515: 'Invalid method',
        516: 'Invalid output format',
        520: 'Database error',
        530: 'User not logged in',
        540: 'Permission denied',
        550: 'Params handling exception',
        # auth exceptions
        560: 'Invalid method',
        561: 'Invalid parameters',
        562: 'Invalid api key',
        563: 'Authorization failed',
        564: 'Other exception'
    }

    def __init__(self, response):
        try:
            self.response = response.json()
        except complexjson.JSONDecodeError:
            raise DeserializeError('Invalid response from livespace API')

    @property
    def data(self):
        return self.response['data']

    @property
    def result(self):
        return self.response['result']

    @property
    def status(self):
        return self.response['status']

    @property
    def error(self):
        return self.response['error']

    def raise_for_status(self):
        if self.result != 200:
            if self.result in self.error_messages.keys():
                raise ApiError(self.result, self.error or self.error_messages
                                                              .get(self.result))
            else:
                raise ApiError(self.result, self.error)


def livespace_authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.access_token = self.get_access_token()
        response = func(*args, **kwargs)
        return response
    return wrapper


class Client(object):

    API_URL_PATTERN = '%(api_url)s/api/public/%(output_format)s/%(module)s/%(method)s'
    AUTH_API_URL_PATTERN = '%(api_url)s/api/public/%(output_format)s/_Api/auth_call/_api_method/getToken'
    options = {
        'auth_method': 'key',
        'return_raw': False
    }

    def __init__(self, api_url, api_key, api_secret, **options):
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.options.update(**options)

    def get_access_token(self, refresh=False):
        url = self._get_auth_endpoint()
        data = {
            '_api_auth': self.options['auth_method'],
            '_api_key': self.api_key
        }
        r = requests.post(url, data=data)
        response = ApiResponse(r)
        response.raise_for_status()
        data = response.data
        return {
            '_api_auth': self.options['auth_method'],
            '_api_key': self.api_key,
            '_api_sha': hashlib.sha1(self.api_key + data['token'] + self.api_secret).hexdigest(),
            '_api_session': data['session_id']
        }

    @livespace_authorize
    def __call__(self, module, method, params={}):
        url = self._get_endpoint(module, method)
        params.update(**self.access_token)
        payload = json.dumps(params)
        r = requests.post(url, {'data': payload})
        response = ApiResponse(r)
        response.raise_for_status()
        return response

    def _get_endpoint(self, module, method):
        return self.API_URL_PATTERN % {
            'api_url': self.api_url,
            'module': module,
            'method': method,
            'output_format': 'json'
        }

    def _get_auth_endpoint(self):
        return self.AUTH_API_URL_PATTERN % {
            'api_url': self.api_url,
            'output_format': 'json'
        }

