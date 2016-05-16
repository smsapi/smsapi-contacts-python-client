# -*- coding: utf-8 -*-

import unittest
from tests import ContactsTestCase
from smsapicontacts.models import CustomFieldModel


class ModelsTest(ContactsTestCase):

    def test_custom_field(self):
        f = self.load_fixture('create_custom_field')['response']

        m = CustomFieldModel.from_dict(f)

        self.assertEqual(f['id'], m.id)
        self.assertEqual(f['name'], m.name)
        self.assertEqual(f['type'], m.type)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ModelsTest))
    return suite