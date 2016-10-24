smsapi-contacts-python
=============

Client for SMSAPI contacts rest api.

## COMPATIBILITY:
Compatible with Python 2.6+, 2.7+, 3.+.

## REQUIREMENTS:
requests

## INSTALLATION:
If You have pip installed:

    sudo pip install smsapi-contacts

else You can install manually:

    git clone https://github.com/smsapi/smsapi-contacts-python-client.git

    cd smsapi-contacts-python

    python setup.py install

## USAGE:

```python
    from smsapicontacts.api import ContactsApi

    api = ContactsApi(username=api_username, password=api_password)
```

#### Contact management

```python
    contact = api.create_contact(
        first_name='Jon', 
        last_name='Doe', 
        idx='id for Your use',
        phone_number=123123123, 
        email='jondoe@somedomain.com'
        birthday_date='1970-01-01',
        gender='{male|female|undefined}',
        city='some_city',
        email='jondoe@somedomain.com',
        source='some_contact_source',
        description='Jon Doe')

    contact = api.update_contact(contact_id=1, description='new_description')
        
    contacts = api.list_contacts()

    contact = api.get_contact(contact_id=1)

    groups = api.list_contact_groups(contact_id=1)

    contact = api.bind_contact_to_group(contact_id=1, group_id=1)
    
    api.delete_contact(contact_id=1)
```

#### Group management

```python
    group = api.create_group(name='group_name', description='group_description')

    groups = api.list_groups()

    group = api.get_group(group_id=1)

    group = api.update_group(group_id=1, name='new_name')

    api.delete_group(group_id=1)

    permissions = api.list_group_permissions(group_id=1)

    permission = api.create_group_permission(
        group_id=1
        read=True,
        write=False,
        send=True)

    permissions = api.list_user_group_permissions(group_id=1, username='some_username')

    api.delete_user_group_permission(group_id=1, username='some_username')

    permission = api.update_user_group_permission(group_id=1, username='some_username', read=False)

    api.unpin_contact_from_group(group_id=1, contact_id=1)

    contact = api.contact_is_in_group(group_id=1, contact_id=1)
```

#### Custom field management

```python
    fields = api.list_custom_fields()

    field = api.create_custom_field(name='some_field_name', type='{TEXT|DATE|EMAIL|NUMBER|PHONENUMBER|}')
    
    field = api.update_custom_field(field_id='1', name='new_field_name')    

    delete_custom_field(field_id=1)
```

#### Error handling

```python
    from smsapicontacts.exception import ContactsApiError

    try:
        contact = api.create_contact(phone_number=123123)
    except ContactsApiError as e:
        print(e.message, e.code, e.type)
```

## LICENSE
[Apache 2.0 License](https://github.com/smsapi/smsapi-contacts-python/blob/master/LICENSE)