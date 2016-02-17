#!/usr/bin/env python
#-*- coding: utf-8 -*-
import mock
import unittest

from livespace import Client
from livespace.exceptions import ApiError


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client('api_url', 'api_key', 'api_secret')
        super(ClientTestCase, self).setUp()

    @mock.patch('requests.post')
    @mock.patch('livespace.Client.get_access_token')
    def test_client_raises_api_error(self, get_access_token, post):
        get_access_token.return_value = {
            '_api_auth': 'key',
            '_api_key': 'api key',
            '_api_session': 'session',
            '_api_sha': 'sha'}

        class MyPost(mock.Mock):
            def json(self):
                return {'data': [], 'error': None, 'result': 561,
                        'status': False}

        post.return_value = MyPost()
        with self.assertRaises(ApiError):
            self.client('Default', 'ping', {'foo': 'bar'})


if __name__ == '__main__':
    unittest.main()
