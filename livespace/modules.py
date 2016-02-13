
class Default(object):

    MODULE_NAME = 'Default'

    def __init__(self, client):
        self.client = client

    def ping(self, **data):
        """
        Takes any params and return them in response.
        Used for testing purpose.
        """
        data = dict(**data)
        return self.client(self.MODULE_NAME, 'ping', data)
