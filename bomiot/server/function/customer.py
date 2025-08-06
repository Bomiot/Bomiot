import orjson

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from bomiot.server.core import models, serializers, filter
from bomiot.server.core.signal import bomiot_data_signals
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from bomiot.server.core.page import DataCorePageNumberPagination
from bomiot.server.core.utils import all_fields_empty, queryset_to_dict, compare_dicts


class CustomerList(ModelViewSet):
    """
        list:
            Response a Customer data list（all）
    """
    pagination_class = DataCorePageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.CustomerFilter

    def get_queryset(self):
        query_params = self.request.query_params.get('params', '')
        if query_params:
            query_str = query_params.replace("'", '"')
            query_str = query_str.replace("true", "True").replace("false", "False")
            query_data = orjson.loads(query_str)
            if all_fields_empty(query_data):
                query_data = {}
        else:
            query_data = {}
        if "is_delete" not in query_data:
            query_data['is_delete'] = False
        if not any(key.startswith('data__department') for key in query_data):
            query_data = {key: value for key, value in query_data.items() if not key.startswith('data__department')}
            if self.request.auth.department == 0:
                department_condition = {"data__department__gte": 0}
            else:
                department_condition = {"data__department__gte": self.request.auth.department}
        else:
            department_condition = {"data__department__gte": self.request.auth.department}
        ordering = query_data.pop('order_by', '-id')
        query_conditions = Q()
        or_conditions = []
        if len(query_data) == 1:
            or_conditions.append(Q(**{**department_condition, "is_delete": query_data['is_delete']}))
        else:
            for key, value in query_data.items():
                if key != 'is_delete':
                    or_conditions.append(Q(**{key: value, **department_condition, "is_delete": query_data['is_delete']}))
        if or_conditions:
            query_conditions &= Q(*or_conditions, _connector=Q.OR)
        return models.Customer.objects.filter(query_conditions).order_by(ordering)

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.CustomerSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class CustomerCreate(ModelViewSet):
    """
    A powerful ViewSet for database management and feedback mechanism
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.CustomerFilter
    queryset = models.Customer.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.CustomerSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, *args, **kwargs):
        """
        Override the create method, combining send_robust and transaction management
        """
        data = self.request.data
        try:
            with transaction.atomic():
                responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                            request=self.request,
                                                            mode='create',
                                                            data=data)
                for receiver, response in responses:
                    if isinstance(response, Exception):
                        raise response
                    if isinstance(response, dict) and response.get("msg"):
                        data['department'] = self.request.auth.department if self.request.auth else 0
                        data['creater'] = self.request.auth.username
                        models.Customer.objects.create(data=data)
                        return Response(response)
                    if isinstance(response, dict) and response.get("detail"):
                        return Response(response)
                    if isinstance(response, dict) and response.get("login"):
                        return Response(response)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class CustomerUpdate(ModelViewSet):
    """
    A powerful ViewSet for database management and feedback mechanism
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.CustomerFilter
    queryset = models.Customer.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action in ['update']:
            return serializers.CustomerSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def update(self, request, *args, **kwargs):
        """
        Override the update method, combining send_robust and transaction management
        """
        data = self.request.data
        db_data = models.Customer.objects.filter(id=data.get('id'), is_delete=False)
        db_check_data = queryset_to_dict(db_data)
        updated_fields = compare_dicts(db_check_data[0], data)
        try:
            with transaction.atomic():
                responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                            request=self.request,
                                                            mode='update',
                                                            data=data,
                                                            updated_fields=updated_fields)
                for receiver, response in responses:
                    if isinstance(response, Exception):
                        raise response
                    if isinstance(response, dict) and response.get("msg"):
                        data.pop('id', None)
                        data.pop('is_delete', None)
                        data.pop('created_time', None)
                        data.pop('updated_time', None)
                        db_data.update(data=data, updated_time=timezone.now())
                        return Response(response)
                    if isinstance(response, dict) and response.get("detail"):
                        return Response(response)
                    if isinstance(response, dict) and response.get("login"):
                        return Response(response)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerDelete(ModelViewSet):
    """
    A powerful ViewSet for database management and feedback mechanism
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.CustomerFilter
    queryset = models.Customer.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action in ['delete']:
            return serializers.CustomerSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method, combining send_robust and transaction management
        """
        data = self.request.data
        db_data = models.Customer.objects.filter(id=data.get('id'), is_delete=False)
        try:
            with transaction.atomic():
                responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                            request=self.request,
                                                            mode='delete',
                                                            data=data)
                for receiver, response in responses:
                    if isinstance(response, Exception):
                        raise response
                    if isinstance(response, dict) and response.get("msg"):
                        db_data.update(is_delete=True, updated_time=timezone.now())
                        return Response(response)
                    if isinstance(response, dict) and response.get("detail"):
                        return Response(response)
                    if isinstance(response, dict) and response.get("login"):
                        return Response(response)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)