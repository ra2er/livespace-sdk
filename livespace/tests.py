#!/usr/bin/env python
#-*- coding: utf-8 -*-
import mock
import unittest

from livespace import Client


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client('api_url', 'api_key', 'api_secret')
        super(ClientTestCase, self).setUp()

    @mock.patch('requests.post')
    def test_client_authorize(self, post):
        pass


if __name__ == '__main__':
    unittest.main()
