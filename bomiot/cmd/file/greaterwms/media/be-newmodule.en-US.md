# Add a New Business Module

Example: adding an "Equipment Management" module from model to frontend.

## 1. Add Model

In `bomiot/server/core/models.py`:

```python
class Equipment(DataCoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_equipment'
        verbose_name = settings.BASE_DB_TABLE + ' Equipment'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

Extends `DataCoreModel` for `project`, `is_delete`, timestamps.

## 2. Add Serializer

In `bomiot/server/core/serializers.py`:

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

## 3. Add Filter

In `bomiot/server/core/filter.py`:

```python
class EquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = models.Equipment
        fields = ['id', 'is_delete']
```

## 4. Add ViewSet

Create `bomiot/server/function/equipment.py`. Follow the pattern from `function/goods.py`:

- `EquipmentList` (GET, with project/department filtering)
- `EquipmentCreate` (POST, sends `bomiot_data_signals` with mode='create')
- `EquipmentUpdate` (POST, sends signal with mode='update')
- `EquipmentDelete` (POST, sends signal with mode='delete')

Key pattern for Create:

```python
class EquipmentCreate(ModelViewSet):
    def create(self, request, *args, **kwargs):
        data = self.request.data
        project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
        with transaction.atomic():
            responses = bomiot_data_signals.send_robust(
                sender=self.__class__, request=self.request, mode='create', data=data
            )
            for receiver, response in responses:
                if isinstance(response, dict) and response.get("msg"):
                    data['department'] = self.request.auth.department
                    data['creater'] = self.request.auth.username
                    models.Equipment.objects.create(data=data, project=project_name)
                    return Response(response)
```

## 5. Register URLs

In `bomiot/server/core/urls.py`:

```python
from bomiot.server.function import equipment

urlpatterns += [
    path(r'equipment/', equipment.EquipmentList.as_view({"get": "list"})),
    path(r'equipment/create/', equipment.EquipmentCreate.as_view({"post": "create"})),
    path(r'equipment/update/', equipment.EquipmentUpdate.as_view({"post": "update"})),
    path(r'equipment/delete/', equipment.EquipmentDelete.as_view({"post": "delete"})),
]
```

## 6. Add Receiver

In `greaterwms/receiver.py`:

```python
from greaterwms.process.equipment import create_equipment_process, update_equipment_process, delete_equipment_process

class EquipmentClass(object):
    def equipment_create(self, data):
        return create_equipment_process(data)

    def equipment_update(self, data):
        return update_equipment_process(data)

    def equipment_delete(self, data):
        return delete_equipment_process(data)
```

## 7. Add Process

Create `greaterwms/process/equipment.py`:

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

## 8. Migrate Database

```bash
bomiot migrate
```

## 9. Frontend Integration

Add routes, menu items, and i18n (see "Add Page" and "Add Menu" guides).

## Checklist

- [ ] Model (extends DataCoreModel)
- [ ] Serializer
- [ ] Filter
- [ ] ViewSet (List/Create/Update/Delete)
- [ ] URL registration
- [ ] Receiver (receiver.py)
- [ ] Process (process/xxx.py)
- [ ] Database migration
- [ ] Frontend route + menu + i18n
