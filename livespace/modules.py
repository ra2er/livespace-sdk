
class Default(object):

    MODULE_NAME = 'Default'

    def __init__(self, client):
        self.client = client

    def ping(self, **params):
        """
        Takes any params and return them in response.
        Used for testing purpose.
        """
        data = dict(**params)
        return self.client(self.MODULE_NAME, 'ping', data)


class Contact(object):

    MODULE_NAME = 'Contact'

    def __init__(self, client):
        self.client = client

    def get_all(self, **params):
        """
        Get all contacts by given criteria.
        Required params:
        :param type: String. e.g.: 'contact'

        All other params are optional.
        This method should be called with at least ONE param.

        :param firstnames: String of comma separated values, e.g.: 'John,Brian'
        :param lastnames: String of comma separated values.
        :param companies: String of comma separated values, e.g.: 'd075b5d4-9e60-8e5b-f436-4bf9c20dfb80' - company ID.
        :param emails: String of comma separated values.
        :param phones: String of comma separated values.

        For date type params pass single date parameter or tuple of date period
        :param created: String or tuple of strings. Datetime ISO format.
        :param modified: String or tuple of strings. Datetime ISO format.
        :param last_active: String or tuple of strings. Datetime ISO format.
        Usage::
            get_all(created='2015-01-01')
            get_all(created=('2015-01-01', '2015-01-20'))

        :param owner_login: String of comma separated values.
        :param condition: e.g: condition='like'; condition='equal'.
        :param tags: String of comma separated values.
        :param tags_condition: String. Tag method filtering: `and` or `or`. Default is `or`.
        :param limit: String representation of INT. Limit of results. Default is all of search results.
        :param offset: String representation of INT. Default is '0'.
        """
        data = {'type': 'contact'}
        data.update(**params)
        return self.client(self.MODULE_NAME, 'getAll', data)

    def get_all_simple(self, **params):
        pass

