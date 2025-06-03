import ast
import orjson

from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from .utils import flatten_json, all_fields_empty
from .signal import bomiot_data_signals


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

