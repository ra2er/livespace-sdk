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

    def filter(self, **params):
        """
        Filter contacts by given criteria. Persons and companies.
        Persons - type: 'contact'
        Companies - type: 'company'

        Takes only one required param:
        :param type: String. e.g.: 'contact' or 'company'

        All other params are optional.
        This method must be called with at least one param.

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
            filter(created='2015-01-01')
            filter(created={'from': '2015-01-01', 'to': '2015-01-20'})

        :param owner_login: String of comma separated values.
        :param condition: e.g: condition='like'; condition='equal'.
        :param tags: String of comma separated values.
        :param tags_condition: String. Tag method filtering: `and` or `or`. Default is `or`.

        :param limit: String representation of INT. Limit of results. Default is all of search results.
        :param offset: String representation of INT. Default is '0'.
        """
        return self.client(self.MODULE_NAME, 'getAll', dict(**params))

    def get_all(self, **params):
        """
        Takes only one required param:
        :param type: String. e.g.: 'contact' or 'company'

        Optional params:
        :param limit: String representation of INT. Limit of results. Default is all of search results.
        :param offset: String representation of INT. Default is '0'.
        """
        return self.client(self.MODULE_NAME, 'getAllSimple', dict(**params))

    def add_contact(self, **params):
        """
        Add person to contacts.
        Usage::
            add_contact(firstname='David', lastname='Novak')
        """
        return self.client(self.MODULE_NAME, 'addContact',
                           {'contact': dict(**params)})

    def add_company(self, **params):
        """
        Add company to contacts.
        Usage::
            add_company(name='Umbrella')

        """
        return self.client(self.MODULE_NAME, 'addCompany',
                           {'company': dict(**params)})

    def add_contact_multiple(self, *contacts):
        """
        Add multiple contacts.
        Usage::
            add_multiple({'firstname': 'David', 'lastname': 'Novak'}, {'firstname': 'John', 'lastname': 'Doe'})
        """
        contacts = {index: contact for index, contact in enumerate(contacts)}
        return self.client(self.MODULE_NAME, 'addContacts',
                           {'contacts': dict(**contacts)})

    def add_company_multiple(self, *companies):
        """
        Add multiple companies.
        Usage::
            add_company_multiple({'name': 'Umbrella'}, {'name': 'Weyland-Yutani'})
        """
        companies = {index: company for index, company in enumerate(companies)}
        return self.client(self.MODULE_NAME, 'addCompanies',
                           {'companies': dict(**companies)})

    def edit_contact(self, id, **params):
        """
        Edit contact of given id and set new params.
        Usage::
            edit_contact('id-of-the-contact', lastname='Novak')
        """
        return self.client(self.MODULE_NAME, 'editContact',
                           {'contact': dict(id=id, **params)})

    def edit_company(self, id, **params):
        """
        Edit company of given id and set new params.
        Usage::
            edit_company('id-of-the-company', name='Umbrella')
        """
        return self.client(self.MODULE_NAME, 'editCompany',
                           {'company': dict(id=id, **params)})

    def add_contact_note(self, id, **params):
        """
        Add note to contact.
        Usage::
            add_contact_note('id-of-contact', note='Some note', tags='tag1,tag2,...,tagN')
        """
        return self.client(self.MODULE_NAME, 'addContactNote',
                           {'contact': dict(id=id, **params)})

    def add_company_note(self, id, **params):
        """
        Add note to company.
        Usage::
            add_contact_note('id-of-contact', note='Some note', tags='tag1,tag2,...,tagN')
        """
        return self.client(self.MODULE_NAME, 'addCompanyNote',
                           {'company': dict(id=id, **params)})

    def delete_contact(self, id):
        """
        Delete contact of given id.
        Usage::
            delete_contact('id-of-contact')
        """
        return self.client(self.MODULE_NAME, 'deleteContact',
                           {'contact': {'id': id}})

    def delete_company(self, id):
        """
        Delete company of given id.
        Usage::
            delete_company('id-of-company')
        """
        return self.client(self.MODULE_NAME, 'deleteCompany',
                           {'company': {'id': id}})

    def get_wall(self, what, id):
        """
        Get wall entries.
        Usage::
            get_wall('contact', 'id-of-contact') or
            get_wall('company', 'id-of-company')
        """
        assert what in ['contact', 'company']
        return self.client(self.MODULE_NAME, 'getWall', {'type': what,
                                                         'id': id})


class Deal(object):

    MODULE_NAME = 'Deal'

    def __init__(self, client):
        self.client = client


class Todo(object):

    MODULE_NAME = 'Todo'

    def __init__(self, client):
        self.client = client


class Search(object):

    MODULE_NAME = 'Search'

    def __init__(self, client):
        self.client = client

    def get_result(self, what, **params):
        """
        Get result of search by given query, other params are also acceptable.
        Usage::
            get_result('contact', q='David') # where q is search queyy
        """
        assert what in ['contact', 'company', 'deal']
        return self.client(self.MODULE_NAME, 'getResult',
                           dict(object_type=what, **params))
