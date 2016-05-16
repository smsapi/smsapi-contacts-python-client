# -*- coding: utf-8 -*-

import os
import json
import unittest
import pkgutil
import requests

from smsapicontacts.compat import is_py26

from tests.doubles import request_fake, TestContactsApi

requests.request = request_fake

api_username = 'must_not_be_empty'
api_password = 'must_not_be_empty'


class ContactsTestCase(unittest.TestCase):

    def setUp(self):
        self.api = TestContactsApi(username=api_username, password=api_password)

    if is_py26:
        def assertIsInstance(self, x, y):
            assert isinstance(x, y), "%r is not instance of %r" % (x, y)

        def assertIsNotNone(self, x):
            assert x is not None, "%x is None" % x

    def load_fixture(self, fixture):
        with open(os.path.abspath(os.path.dirname(__file__)) + '/fixtures/%s.json' % fixture) as f:
            data = f .read()

        return json.loads(data)


def import_from_string(name):

    if '.' in name:
        module, pkg = name.rsplit(".", 1)
    else:
        return __import__(name)

    return getattr(__import__(module, None, None, [pkg]), pkg)


def app_test_suites():

    module = import_from_string(__name__)

    path = getattr(module, '__path__', None)

    if not path:
        raise ValueError('%s is not a package' % module)

    basename = module.__name__ + '.'

    for importer, module_name, is_pkg in pkgutil.iter_modules(path):
        mod = basename + module_name

        module = import_from_string(mod)

        if hasattr(module, 'suite'):
            yield module.suite()


def suite():
    suite = unittest.TestSuite()
    for _suite in app_test_suites():
        suite.addTest(_suite)
    return suite


def run_tests():
    try:
        unittest.TextTestRunner(verbosity=2).run(suite())
    except Exception as e:
        print('Error: %s' % e)


if __name__ == '__main__':
    run_tests()