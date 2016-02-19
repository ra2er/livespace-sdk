#-*- coding: utf-8 -*-

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
        Takes only one required param which is set by default:
        :param type: String. e.g.: 'contact'

        All other params are optional.
        This method must be called with at least ONE param.

        :param firstnames: String of comma separated values, e.g.: 'John,Brian'
        :param lastnames: String of comma separated values.
        :param companies: String of comma separated values, e.g.: 'd075b5d4-9e60-8e5b-f436-4bf9c20dfb80' - company ID.
        :param emails: String of comma separated values.
        :param phones: String of comma separated values.

        For date type params pass single date parameter or dict of date period
        :param created: String or tuple of strings. Datetime ISO format.
        :param modified: String or tuple of strings. Datetime ISO format.
        :param last_active: String or tuple of strings. Datetime ISO format.
        Usage::
            get_all(created='2015-01-01')
            get_all(created={'from': '2015-01-01', 'to': '2015-01-20'})

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
        """
        Same as get all but with reduced number of params.
        Takes only one required param which is set by default:
        :param type: String. e.g.: 'contact'

        Optional params:
        :param limit: String representation of INT. Limit of results. Default is all of search results.
        :param offset: String representation of INT. Default is '0'.
        """
        data = {'type': 'contact'}
        limit = params.get('limit')
        offset = params.get('offset')
        if limit:
            data.updata(limit=limit)
        if offset:
            data.update(offset=offset)
        return self.client(self.MODULE_NAME, 'getAllSimple', data)

    def add(self, **params):
        """
        Usage::
            add(firstname='David', lastname='Novak')
        """
        return self.client(self.MODULE_NAME, 'addContact',
                           {'contact': dict(**params)})

    def add_multiple(self, *contacts):
        """
        Add multiple contacts.
        Like `add` but takes list of contacts. Each contact is a dict with contact fields.
        Usage::
            add_multiple({'firstname': 'David', 'lastname': 'Novak'}, {'firstname': 'John', 'lastname': 'Doe'})
        """
        contacts = {index: contact for index, contact in enumerate(contacts)}
        return self.client(self.MODULE_NAME, 'addContacts',
                           {'contacts': dict(**contacts)})

    def delete(self, id):
        """
        :param id: String. e.g.: 'd075b5d4-9e60-8e5b-f436-4bf9c20dfb80' - contact ID.
        """
        return self.client(self.MODULE_NAME, 'deleteContacts',
                           {'contact': {'id': id}})

    def edit(self, id, **params):
        """
        Edit contact of given id and set new params.
        Usage::
            edit('id-of-the-contact', lastname='Novak')
        """
        data = {'id': id}
        data.updata(**params)
        return self.client(self.MODULE_NAME, 'editContact', {'contact': data})


