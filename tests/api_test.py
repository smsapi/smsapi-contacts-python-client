# -*- coding: utf-8 -*-

import unittest

from datetime import datetime, date

from smsapicontacts.models import ContactModel, GroupModel, GroupPermissionModel, ModelCollection, CustomFieldModel
from smsapicontacts.exception import ContactsApiError

from tests import ContactsTestCase
from tests.doubles import ResponseMock


class ContactsApiErrorTest(ContactsTestCase):

    def setUp(self):
        super(ContactsApiErrorTest, self).setUp()
        ResponseMock.force_status_code = 500

    def tearDown(self):
        super(ContactsApiErrorTest, self).tearDown()
        ResponseMock.force_status_code = None

    def test_error_when_no_path_parameter_found(self):
        self.assertRaises(ContactsApiError, self.api.update_contact)

    def test_error_if_http_status_code_not_in_range_of_success_codes(self):
        self.assertRaises(ContactsApiError, self.api.update_contact, contact_id=1)


class ContactsApiTest(ContactsTestCase):

    def test_create_contact(self):
        contact = self.api.create_contact(
            first_name='Jon',
            phone_number=987654321,
            email='jondoe@somedomain.com')

        self.assertIsInstance(contact, ContactModel)
        self.assertIsInstance(contact.date_created, datetime)
        self.assertIsInstance(contact.birthday_date, date)

    def test_update_contact(self):
        contact = self.api.update_contact(contact_id=1, last_name='Doe')

        self.assertEqual(contact.last_name, 'Doe')

    def test_list_contacts(self):
        contacts = self.api.list_contacts()

        self.assertIsInstance(contacts, ModelCollection)
        self.assertEqual(len(contacts), 2)

        for c in contacts:
            self.assertIsInstance(c, ContactModel)

    def test_get_contact(self):
        self.api.get_contact(contact_id=1)

    def test_delete_contact(self):
        self.api.delete_contact(contact_id=1)

    def test_list_contacts_groups(self):
        self.api.list_contact_groups(contact_id=1)

    def test_bind_contact_to_group(self):
        self.api.bind_contact_to_group(contact_id=1, group_id=1)

    def test_list_groups(self):
        self.api.list_groups()

    def test_create_group(self):
        self.api.create_group()

    def test_delete_group(self):
        self.api.delete_group(group_id=1)

    def test_get_group(self):
        group = self.api.get_group(group_id=1)

        self.assertIsInstance(group, GroupModel)
        self.assertIsInstance(group.permissions, list)

        for p in group.permissions:
            self.assertIsInstance(p, GroupPermissionModel)

    def test_update_group(self):
        self.api.update_group(group_id=1)

    def test_list_group_permission(self):
        self.api.list_group_permissions(group_id=1)

    def test_create_group_permission(self):
        self.api.create_group_permission(group_id=1)

    def test_list_user_group_permission(self):
        self.api.list_user_group_permissions(group_id=1, username='test')

    def test_delete_user_group_permission(self):
        self.api.delete_user_group_permission(group_id=1, username='test')

    def test_update_user_group_permission(self):
        self.api.update_user_group_permission(group_id=1, username='test')

    def test_unpin_contact_from_group(self):
        self.api.unpin_contact_from_group(group_id=1, contact_id=1)

    def test_contact_is_in_group(self):
        self.api.contact_is_in_group(group_id=1, contact_id=1)

    def test_pin_contact_to_group(self):
        self.api.pin_contact_to_group(group_id=1, contact_id=1)

    def test_list_custom_fields(self):
        r = self.api.list_custom_fields()

        fixture = self.load_fixture('list_custom_fields')['response']['collection'][0]

        self.assertIsInstance(r, ModelCollection)
        self.assertEqual(r[0], CustomFieldModel.from_dict(fixture))

    def test_create_custom_field(self):
        self.api.create_custom_field()

    def test_delete_custom_field(self):
        self.api.delete_custom_field(field_id=1)

    def test_update_custom_field(self):
        self.api.update_custom_field(field_id=1, name='test_f')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContactsApiTest))
    suite.addTest(unittest.makeSuite(ContactsApiErrorTest))
    return suite