# -*- coding: utf-8 -*-

import re
import requests

from . import lib_info
from .compat import quote, py_version
from .utils import convert_to_utf8_str, is_http_success
from .exception import ContactsApiError


def bind_api_endpoint(**config):

    class ApiEndpoint(object):

        method = config.get('method')

        path = config.get('path')

        response_mapping = config.get('mapping')

        accept_parameters = config.get('accept_parameters')

        def __init__(self, api, parameters):

            super(ApiEndpoint, self).__init__()

            self.api = api

            self.parameters = parameters

            self.filter_parameters()
            self.compile_path()

        def filter_parameters(self):

            compiled_parameters = {}

            for key, val in self.parameters.items():
                if key in self.accept_parameters:
                    compiled_parameters[key] = convert_to_utf8_str(val)

            self.parameters = compiled_parameters

        def compile_path(self):

            placeholder_pattern = re.compile('{\w+}')

            for placeholder in placeholder_pattern.findall(self.path):
                name = placeholder.strip('{}')

                if name in self.parameters:
                    param = quote(self.parameters.pop(name))
                    self.path = self.path.replace(placeholder, param)
                else:
                    raise ContactsApiError("No parameter found for path variable '%s'" % name)

        def send_request(self):

            url = '%s%s' % (self.api.host, self.path)

            headers = {
                'User-Agent': '%s (Python%s)' % (lib_info, py_version)
            }

            raw_response = requests.request(self.method, url, data=self.parameters, auth=self.api.auth, headers=headers)

            return self.process_response(raw_response)

        def process_response(self, raw_response):

            response = raw_response.json()

            if not is_http_success(raw_response.status_code):
                raise ContactsApiError.from_dict(response)

            if isinstance(self.response_mapping, tuple):
                model, type = self.response_mapping
                response = type.parse(response, model)
            elif self.response_mapping:
                response = self.response_mapping.from_dict(response)

            return response

    def __call(api, **kwargs):
        endpoint = ApiEndpoint(api, kwargs)
        return endpoint.send_request()

    return __call