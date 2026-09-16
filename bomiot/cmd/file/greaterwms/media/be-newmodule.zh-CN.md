# 新增业务模块

以新增一个「设备管理」模块为例，演示从模型到前端的完整开发流程。

## 1. 新增模型

在 `bomiot/server/core/models.py` 添加模型：

```python
class Equipment(DataCoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_equipment'
        verbose_name = settings.BASE_DB_TABLE + ' Equipment'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

> 继承 `DataCoreModel`，自动获得 `project`、`is_delete`、`created_time`、`updated_time` 字段。

## 2. 新增 Serializer

在 `bomiot/server/core/serializers.py` 添加：

```python
class EquipmentSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(read_only=True, required=False)
    project = serializers.CharField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Equipment
        fields = ['id', 'data', 'project', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']
```

## 3. 新增 Filter

在 `bomiot/server/core/filter.py` 添加：

```python
class EquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = models.Equipment
        fields = ['id', 'is_delete']
```

## 4. 新增 ViewSet

在 `bomiot/server/function/equipment.py`（新建文件）中编写：

```python
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
from django.conf import settings
from django.db.models import Q
from bomiot.server.core.page import DataCorePageNumberPagination
from bomiot.server.core.utils import all_fields_empty, queryset_to_dict, compare_dicts


class EquipmentList(ModelViewSet):
    pagination_class = DataCorePageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["id", "created_time", "updated_time"]
    filter_class = filter.EquipmentFilter

    def get_queryset(self):
        project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
        if project_name.lower() == 'bomiot':
            project_name = settings.PROJECT_NAME
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
        if self.request.auth.department == 0:
            department_condition = {"data__department__gte": 0}
        else:
            department_condition = {"data__department__gte": self.request.auth.department}
        query_data = {k: v for k, v in query_data.items() if not k.startswith('data__department')}
        ordering = query_data.pop('order_by', '-id')
        query_conditions = Q()
        or_conditions = []
        if len(query_data) == 1:
            or_conditions.append(Q(**{**department_condition, "is_delete": query_data['is_delete'], "project": project_name}))
        else:
            for key, value in query_data.items():
                if key != 'is_delete':
                    or_conditions.append(Q(**{key: value, **department_condition, "is_delete": query_data['is_delete'], "project": project_name}))
        if or_conditions:
            query_conditions &= Q(*or_conditions, _connector=Q.OR)
        return models.Equipment.objects.filter(query_conditions).order_by(ordering)

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.EquipmentSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class EquipmentCreate(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id', "created_time", "updated_time"]
    filter_class = filter.EquipmentFilter
    queryset = models.Equipment.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.EquipmentSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
        if project_name.lower() == 'bomiot':
            project_name = settings.PROJECT_NAME
        try:
            with transaction.atomic():
                responses = bomiot_data_signals.send_robust(
                    sender=self.__class__,
                    request=self.request,
                    mode='create',
                    data=data
                )
                for receiver, response in responses:
                    if isinstance(response, Exception):
                        raise response
                    if isinstance(response, dict) and response.get("msg"):
                        data['department'] = self.request.auth.department if self.request.auth else 0
                        data['creater'] = self.request.auth.username
                        models.Equipment.objects.create(data=data, project=project_name)
                        return Response(response)
                    if isinstance(response, dict) and response.get("detail"):
                        return Response(response)
                    if isinstance(response, dict) and response.get("login"):
                        return Response(response)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            with transaction.atomic():
                transaction.set_rollback(True)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
```

> Update/Delete 类似，参照 `function/goods.py`。

## 5. 注册 URL

在 `bomiot/server/core/urls.py` 添加：

```python
from bomiot.server.function import equipment

urlpatterns += [
    path(r'equipment/', equipment.EquipmentList.as_view({"get": "list"}), name="Get Equipment List"),
    path(r'equipment/create/', equipment.EquipmentCreate.as_view({"post": "create"}), name="Create Equipment"),
    path(r'equipment/update/', equipment.EquipmentUpdate.as_view({"post": "update"}), name="Update Equipment"),
    path(r'equipment/delete/', equipment.EquipmentDelete.as_view({"post": "delete"}), name="Delete Equipment"),
]
```

## 6. 新增 Receiver

在项目 `receiver.py` 中添加：

```python
from greaterwms.process.equipment import create_equipment_process, update_equipment_process, delete_equipment_process

class EquipmentClass(object):
    def equipment_create(self, data):
        context = create_equipment_process(data)
        return context

    def equipment_update(self, data):
        context = update_equipment_process(data)
        return context

    def equipment_delete(self, data):
        context = delete_equipment_process(data)
        return context
```

## 7. 新增 Process

新建 `greaterwms/process/equipment.py`：

```python
from bomiot.server.core.message import msg_message_return, detail_message_return
from bomiot.server.core.models import Equipment
from django.contrib.auth import get_user_model

User = get_user_model()


def create_equipment_process(data):
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    user_info = User.objects.filter(id=data.get('request').auth.id).first()
    equip_check = Equipment.objects.filter(
        data__code=data.get('data').get('code'),
        data__department=user_info.department,
        is_delete=False
    ).first()
    if equip_check is not None:
        return detail_message_return(language, "Equipment already exists")
    return msg_message_return(language, "Success Create")
```

## 8. 数据库迁移

```bash
bomiot migrate
```

## 9. 前端对接

在前端添加路由、菜单、i18n（参照「新增页面」和「新增菜单」文档）。

## 清单

- [ ] Model（继承 DataCoreModel）
- [ ] Serializer
- [ ] Filter
- [ ] ViewSet（List/Create/Update/Delete）
- [ ] URL 注册
- [ ] Receiver（receiver.py）
- [ ] Process（process/xxx.py）
- [ ] 数据库迁移
- [ ] 前端路由 + 菜单 + i18n
