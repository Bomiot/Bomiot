import ast
import orjson
import time
from os.path import join, exists
from tomlkit import parse
import random

from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from django.conf import settings
from django.core.cache import cache
from .utils import flatten_json, all_fields_empty
from .signal import bomiot_data_signals
from .models import Permission
from .message import permission_message_return

class CorePageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000

    def get_previous_link(self):
        """
        get previous link
        :return: previous link whole URL or None
        """
        if not self.page.has_previous():
            return None
        return self._build_absolute_url(self.page.previous_page_number())

    def get_next_link(self):
        """
        get next link
        :return: next link whole URL or None
        """
        if not self.page.has_next():
            return None
        return self._build_absolute_url(self.page.next_page_number())

    def _build_absolute_url(self, page_number):
        """
        resoleve absolute URL
        :param page_number: page number
        :return: full URL
        """
        url = self.request.build_absolute_uri()
        ssl_scheme = self.request.scheme
        url_parts = str(url).split(':', 1)

        if url_parts[0] == ssl_scheme:
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            # Fix URL SSL scheme
            corrected_url = f"{ssl_scheme}:{url_parts[1]}"
            return replace_query_param(corrected_url, self.page_query_param, page_number)
        
    def query_data_add(self) -> list:
        return []

    def get_paginated_response(self, data):
        response_data = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]
        response_data += self.query_data_add()
        return Response(OrderedDict(response_data))


class PermissionPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 1000
    page_size_query_param = "max_page"
    max_page_size = 10000
    time_ns = int(time.time_ns()) + random.randint(0, 10000)

    def get_previous_link(self):
        """
        get previous link
        :return: previous link whole URL or None
        """
        if not self.page.has_previous():
            return None
        return self._build_absolute_url(self.page.previous_page_number())

    def get_next_link(self):
        """
        get next link
        :return: next link whole URL or None
        """
        if not self.page.has_next():
            return None
        return self._build_absolute_url(self.page.next_page_number())

    def _build_absolute_url(self, page_number):
        """
        resoleve absolute URL
        :param page_number: page number
        :return: full URL
        """
        url = self.request.build_absolute_uri()
        ssl_scheme = self.request.scheme
        url_parts = str(url).split(':', 1)

        if url_parts[0] == ssl_scheme:
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            # Fix URL SSL scheme
            corrected_url = f"{ssl_scheme}:{url_parts[1]}"
            return replace_query_param(corrected_url, self.page_query_param, page_number)
        
    def query_data_add(self) -> list:
        return []
    
    def get_permission_return_data(self, data) -> dict:
        permission_data = cache.get("permission_message", version=self.time_ns)
        if data.get('name') in permission_data:
            return {
                "label": permission_data.get(data.get('name')),
                "value": data.get('name')
            }
        else:
            return {
                "label": data.get('name'),
                "value": data.get('name')
            }

    def get_paginated_response(self, data):
        language = self.request.META.get('HTTP_LANGUAGE', 'en-US')
        message_path = join(settings.LANGUAGE_DIR, language + '.toml')
        message_dict = {}
        if exists(message_path):
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
        message_dict = message_data['permission']
        cache.set('permission_message', orjson.loads(orjson.dumps(message_dict).decode("utf-8")), version=self.time_ns)
        data_list = list(map(lambda x: self.get_permission_return_data(x), data))
        cache.delete("permission_message", version=self.time_ns)
        response_data = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data_list)
        ]
        response_data += self.query_data_add()
        return Response(OrderedDict(response_data))


class TeamPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000
    time_ns = int(time.time_ns()) + random.randint(0, 10000)

    def get_previous_link(self):
        """
        get previous link
        :return: previous link whole URL or None
        """
        if not self.page.has_previous():
            return None
        return self._build_absolute_url(self.page.previous_page_number())

    def get_next_link(self):
        """
        get next link
        :return: next link whole URL or None
        """
        if not self.page.has_next():
            return None
        return self._build_absolute_url(self.page.next_page_number())

    def _build_absolute_url(self, page_number):
        """
        resoleve absolute URL
        :param page_number: page number
        :return: full URL
        """
        url = self.request.build_absolute_uri()
        ssl_scheme = self.request.scheme
        url_parts = str(url).split(':', 1)

        if url_parts[0] == ssl_scheme:
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            # Fix URL SSL scheme
            corrected_url = f"{ssl_scheme}:{url_parts[1]}"
            return replace_query_param(corrected_url, self.page_query_param, page_number)
        
    def query_data_add(self) -> list:
        return []
    
    def get_permission_return_data(self, data) -> dict:
        permission_message = cache.get("permission_message", version=self.time_ns)
        if data.name in permission_message:
            return {
                "label": permission_message.get(data.name),
                "value": data.name
            }
        else:
            return {
                "label": data.name,
                "value": data.name
            }

    def get_paginated_response(self, data):
        language = self.request.META.get('HTTP_LANGUAGE', 'en-US')
        message_path = join(settings.LANGUAGE_DIR, language + '.toml')
        message_dict = {}
        if exists(message_path):
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
        message_dict = message_data['permission']
        cache.set('permission_message', orjson.loads(orjson.dumps(message_dict).decode("utf-8")), version=self.time_ns)
        permission_list = Permission.objects.filter()
        permission_data_list = list(map(lambda x: self.get_permission_return_data(x), permission_list))
        cache.delete("permission_message", version=self.time_ns)
        response_data = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('permission_list', permission_data_list),
            ('results', data)
        ]
        response_data += self.query_data_add()
        return Response(OrderedDict(response_data))


class DataCorePageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000

    def get_previous_link(self):
        """
        get previous link
        :return: previous link whole URL or None
        """
        if not self.page.has_previous():
            return None
        return self._build_absolute_url(self.page.previous_page_number())

    def get_next_link(self):
        """
        get next link
        :return: next link whole URL or None
        """
        if not self.page.has_next():
            return None
        return self._build_absolute_url(self.page.next_page_number())

    def _build_absolute_url(self, page_number):
        """
        resoleve absolute URL
        :param page_number: page number
        :return: full URL
        """
        url = self.request.build_absolute_uri()
        ssl_scheme = self.request.scheme
        url_parts = str(url).split(':', 1)

        if url_parts[0] == ssl_scheme:
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            # Fix URL SSL scheme
            corrected_url = f"{ssl_scheme}:{url_parts[1]}"
            return replace_query_param(corrected_url, self.page_query_param, page_number)
        
    def get_paginated_response(self, data):
        response_data = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ]
        data_list = list(map(lambda x: flatten_json(x) if isinstance(x, dict) else x, data))
        origin = self.request.query_params.dict()
        params_check = self.request.query_params.get('params', {})
        if params_check:
            params_str = params_check.replace('true', 'True').replace('false', 'False')
            params_str = params_check.replace("'", '"')
            params_dict = ast.literal_eval(params_str)
            if all_fields_empty(params_dict):
                origin['params'] = {}
            origin['params'] = params_dict
        else:
            origin['params'] = {}
        responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                    request=self.request,
                                                    mode='get',
                                                    query_params=origin,
                                                    data=data_list)
        for receiver, response in responses:
            if isinstance(response, Exception):
                raise response
            if isinstance(response, list):
                callback_data = True
                for i in response:
                    if i[0] == 'results':
                        callback_data = False
                        break
                    else:
                        continue
                if callback_data is False:
                    response_data += [('results', data_list)]
                response_data += response
        return Response(OrderedDict(response_data))


class APIPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000
    time_ns = int(time.time_ns()) + random.randint(0, 10000)

    def get_previous_link(self):
        """
        get previous link
        :return: previous link whole URL or None
        """
        if not self.page.has_previous():
            return None
        return self._build_absolute_url(self.page.previous_page_number())

    def get_next_link(self):
        """
        get next link
        :return: next link whole URL or None
        """
        if not self.page.has_next():
            return None
        return self._build_absolute_url(self.page.next_page_number())

    def _build_absolute_url(self, page_number):
        """
        resoleve absolute URL
        :param page_number: page number
        :return: full URL
        """
        url = self.request.build_absolute_uri()
        ssl_scheme = self.request.scheme
        url_parts = str(url).split(':', 1)

        if url_parts[0] == ssl_scheme:
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            # Fix URL SSL scheme
            corrected_url = f"{ssl_scheme}:{url_parts[1]}"
            return replace_query_param(corrected_url, self.page_query_param, page_number)
        
    def query_data_add(self) -> list:
        return []

    def get_api_return_data(self, data) -> dict:
        permission_data = cache.get("permission_message", version=self.time_ns)
        if data.get('name') in permission_data:
            data['name'] = permission_data.get(data.get('name'))
        return data
    
    def get_paginated_response(self, data):
        language = self.request.META.get('HTTP_LANGUAGE', 'en-US')
        message_path = join(settings.LANGUAGE_DIR, language + '.toml')
        message_dict = {}
        if exists(message_path):
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
        message_dict = message_data['permission']
        cache.set('permission_message', orjson.loads(orjson.dumps(message_dict).decode("utf-8")), version=self.time_ns)
        data_list = list(map(lambda x: self.get_api_return_data(x), data))
        cache.delete("permission_message", version=self.time_ns)
        response_data = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data_list)
        ]
        response_data += self.query_data_add()
        return Response(OrderedDict(response_data))