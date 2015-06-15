# -*- coding: utf-8 -*-

from requests.auth import HTTPBasicAuth

from .exception import ContactsApiError
from .endpoint import bind_api_endpoint
from .models import ContactModel, GroupModel, GroupPermissionModel, CustomFieldModel, ModelCollection

list_params = ['offset' 'limit', 'orderBy']

contact_params = ['first_name', 'last_name', 'phone_number', 'email',
                  'gender', 'birthday_date', 'description']


class ContactsApi(object):

    host = 'https://api.smsapi.pl/'

    def __init__(self, **kwargs):
        """
        Args:
            username (string): Api username.
            password (string): Api password in plain text format.
            auth (object): Auth handler, default BasicAuth.
        """

        super(ContactsApi, self).__init__()

        username = kwargs.get('username')
        password = kwargs.get('password')

        if not any((username, password)):
            raise ContactsApiError('Authorization data required.')

        self.auth = HTTPBasicAuth(username, password)

    list_contacts = bind_api_endpoint(
        method='GET',
        path='contacts',
        mapping=(ContactModel, ModelCollection),
        accept_parameters=contact_params + list_params + ['q']
    )

    get_contact = bind_api_endpoint(
        method='GET',
        path='contacts/{contact_id}',
        mapping=ContactModel,
        accept_parameters=['contact_id']
    )

    update_contact = bind_api_endpoint(
        method='PUT',
        path='contacts/{contact_id}',
        mapping=ContactModel,
        accept_parameters=contact_params + ['contact_id']
    )

    create_contact = bind_api_endpoint(
        method='POST',
        path='contacts',
        mapping=ContactModel,
        accept_parameters=contact_params
    )

    delete_contact = bind_api_endpoint(
        method='DELETE',
        path='contacts/{contact_id}',
        accept_parameters=['contact_id']
    )

    list_contact_groups = bind_api_endpoint(
        method='GET',
        path='contacts/{contact_id}/groups',
        mapping=(GroupModel, ModelCollection),
        accept_parameters=['contact_id', 'group_id']
    )

    bind_contact_to_group = bind_api_endpoint(
        method='POST',
        path='contacts/{contact_id}/groups/{group_id}',
        accept_parameters=['contact_id', 'group_id']
    )

    list_groups = bind_api_endpoint(
        method='GET',
        path='contacts/groups',
        mapping=(GroupModel, ModelCollection),
        accept_parameters=['group_id', 'name']
    )

    create_group = bind_api_endpoint(
        method='POST',
        path='contacts/groups',
        mapping=GroupModel,
        accept_parameters=['name', 'description', 'idx']
    )

    delete_group = bind_api_endpoint(
        method='DELETE',
        path='contacts/groups/{group_id}',
        accept_parameters=['group_id']
    )

    get_group = bind_api_endpoint(
        method='GET',
        path='contacts/groups/{group_id}',
        mapping=GroupModel,
        accept_parameters=['group_id']
    )

    update_group = bind_api_endpoint(
        method='PUT',
        path='contacts/groups/{group_id}',
        mapping=GroupModel,
        accept_parameters=['group_id', 'name', 'description', 'idx']
    )

    list_group_permissions = bind_api_endpoint(
        method='GET',
        path='contacts/groups/{group_id}/permissions',
        mapping=GroupPermissionModel,
        accept_parameters=['group_id']
    )

    create_group_permission = bind_api_endpoint(
        method='POST',
        path='contacts/groups/{group_id}/permissions',
        mapping=GroupPermissionModel,
        accept_parameters=['group_id', 'username', 'read', 'write', 'send']
    )

    list_user_group_permissions = bind_api_endpoint(
        method='GET',
        path='contacts/groups/{group_id}/permissions/{username}',
        mapping=(GroupPermissionModel, ModelCollection),
        accept_parameters=['group_id', 'username']
    )

    delete_user_group_permission = bind_api_endpoint(
        method='DELETE',
        path='contacts/groups/{group_id}/permissions/{username}',
        accept_parameters=['group_id', 'username']
    )

    update_user_group_permission = bind_api_endpoint(
        method='PUT',
        path='contacts/groups/{group_id}/permissions/{username}',
        mapping=GroupPermissionModel,
        accept_parameters=['group_id', 'username', 'read', 'write', 'send']
    )

    unpin_contact_from_group = bind_api_endpoint(
        method='DELETE',
        path='contacts/groups/{group_id}/members/{contact_id}',
        accept_parameters=['group_id', 'contact_id']
    )

    contact_is_in_group = bind_api_endpoint(
        method='GET',
        path='contacts/groups/{group_id}/members/{contact_id}',
        mapping=ContactModel,
        accept_parameters=['group_id', 'contact_id']
    )

    pin_contact_to_group = bind_api_endpoint(
        method='PUT',
        path='contacts/groups/{group_id}/members/{contact_id}',
        mapping=ContactModel,
        accept_parameters=['group_id', 'contact_id']
    )

    list_custom_fields = bind_api_endpoint(
        method='GET',
        mapping=(CustomFieldModel, ModelCollection),
        path='contacts/fields'
    )

    create_custom_field = bind_api_endpoint(
        method='POST',
        path='contacts/fields',
        mapping=CustomFieldModel,
        accept_parameters=['name', 'type']
    )

    delete_custom_field = bind_api_endpoint(
        method='DELETE',
        path='contacts/fields',
        accept_parameters=['field_id']
    )

    update_custom_field = bind_api_endpoint(
        method='PUT',
        path='contacts/fields',
        mapping=CustomFieldModel,
        accept_parameters=['name', 'type']
    )