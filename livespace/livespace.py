from requests.exceptions import HTTPError
from functools import wraps
import hashlib
import json
import requests


class ApiError(Exception):

    pass


def livespace_authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.access_token = self.get_access_token()
        try:
            response = func(*args, **kwargs)
            if response.result == 563: # 563 is unauthorized
                # get auth token
                self.access_token = self.get_access_token(refresh=True)
                response = func(*args, **kwargs)
            else:
                raise ApiError()
        except HTTPError:
            raise
        return response
    return wrapper


class Client(object):

    API_URL_PATTERN = '%(api_url)s/api/public/%(output_format)s/%(module)s/%(method)s'
    AUTH_API_URL_PATTERN = '%(api_url)s/api/public/%(output_format)s/_Api/auth_call/_api_method/getToken'
    options = {
        'format': 'json',
        'auth_method': 'key',
        'return_raw': False
    }

    def __init__(self, api_url, api_key, api_secret, **options):
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.options.update(**options)

    def get_access_token(self, refresh=False):
        access_token = getattr(self, 'access_token', None)
        if access_token and not refresh:
            return access_token
        url = self._get_auth_endpoint()
        data = {
            '_api_auth': self.options['auth_method'],
            '_api_key': self.api_key
        }
        r = requests.post(url, data=data)
        data = r.json()['data']
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
        return  r.json()

    def _get_endpoint(self, module, method):
        return self.API_URL_PATTERN % {
            'api_url': self.api_url,
            'module': module,
            'method': method,
            'output_format': self.options['format']
        }

    def _get_auth_endpoint(self):
        return self.AUTH_API_URL_PATTERN % {
            'api_url': self.api_url,
            'output_format': self.options['format']
        }


