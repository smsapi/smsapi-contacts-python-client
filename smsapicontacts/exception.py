# -*- coding: utf-8 -*-


class ContactsApiError(Exception):

    def __init__(self, message, code=None, type=None, errors=None):

        super(ContactsApiError, self).__init__(message)

        self.message = message
        self.code = code or ''
        self.type = type
        self.errors = errors

    @classmethod
    def from_dict(cls, data):
        """
        Create ContactsApiError instance from dictionary.

        Args:
            data (dict)
        """

        code = data.get('code')
        type = data.get('type')
        message = data.get('message')

        return cls(message, code, type)

    def __str__(self):
        return '%s %s' % (self.code, self.message)