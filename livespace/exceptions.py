#-*- coding: utf-8 -*-

class DeserializeError(Exception):

    pass


class ApiError(Exception):

    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return '%s: %s' % (self.status_code, self.message)


class ApiMethodError(ApiError):
    """ Status code: 550 """

    def __init__(self, status_code, response_error, **kwargs):
        super(ApiMethodError, self).__init__(status_code, response_error, **kwargs)
        self.response_error = response_error

    def __str__(self):
        # livespace API returns unicode encoded strings as error descriptions
        message = self.message or ' '.join(['%s - %s' % (k, v.encode('ascii',
                                                                     'replace'))
                                            for (k, v) in (self.response_error
                                                               .items())])
        return '%s: %s' % (self.status_code, message)

