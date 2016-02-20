#-*- coding:: utf-8 -*-
from requests.models import complexjson
import hashlib
import json
import requests

from . import modules, exceptions


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
            raise exceptions.DeserializeError('Invalid response from livespace API')

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
                if self.result == 550:
                    raise exceptions.ApiMethodError(self.result, self.error)
                raise exceptions.ApiError(self.result, self.error_messages
                                                           .get(self.result))
            else:
                raise exceptions.ApiError(self.result, self.error)


class Client(object):

    API_URL_PATTERN = '%(api_url)s/api/public/%(output_format)s/%(module)s/%(method)s'
    AUTH_API_URL_PATTERN = '%(api_url)s/api/public/%(output_format)s/_Api/auth_call/_api_method/getToken'

    def __init__(self, api_url, api_key, api_secret):
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret

    def get_access_token(self, refresh=False):
        url = self._get_auth_endpoint()
        data = {
            '_api_auth': 'key',
            '_api_key': self.api_key
        }
        r = requests.post(url, data=data)
        response = ApiResponse(r)
        response.raise_for_status()
        data = response.data
        return {
            '_api_auth': 'key',
            '_api_key': self.api_key,
            '_api_sha': hashlib.sha1(self.api_key + data['token'] + self.api_secret).hexdigest(),
            '_api_session': data['session_id']
        }

    def __call__(self, module, method, params={}):
        url = self._get_endpoint(module, method)
        token = self.get_access_token()
        params.update(**token)
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


class Api(object):

    def __init__(self, client):
        self.client = client
        self.default = modules.Default(client)
        self.contact = modules.Contact(client)
        self.deal = modules.Deal(client)
        self.todo = modules.Todo(client)
        self.search = modules.Search(client)


    @classmethod
    def construct(cls, api_url, api_key, api_secret):
        client = Client(api_url, api_key, api_secret)
        return cls(client=client)

