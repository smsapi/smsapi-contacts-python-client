# -*- coding: utf-8 -*-

import os
import json
import types

from smsapicontacts.api import ContactsApi

last_called_api_method = None


def request_fake(*args, **kwargs):
    """
    Fake request object map api method call to fixtures json file.
    """

    dir = os.path.abspath(os.path.dirname(__file__))

    with open('%s/fixtures/%s.json' % (dir, last_called_api_method)) as f:
        response = json.loads(f.read())

    status_code = response.get('status_code')
    content = response.get('response')

    return ResponseMock(status_code, content)


class ResponseMock(object):

    force_status_code = None

    def __init__(self, status_code, content):
        super(ResponseMock, self).__init__()

        self.code = status_code
        self.content = content

    @property
    def status_code(self):
        if self.force_status_code:
            return self.force_status_code
        return self.code

    def json(self):
        return self.content


class TestContactsApi(ContactsApi):

    def __getattribute__(self, item):
        """
        Track access to ContactsApi class methods to save last called name.
        """

        global last_called_api_method

        attr = super(TestContactsApi, self).__getattribute__(item)

        if isinstance(attr, types.MethodType):
            last_called_api_method = item

        return attr