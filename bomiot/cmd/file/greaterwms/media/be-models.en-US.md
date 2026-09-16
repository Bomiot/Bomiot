# Model Design

## Two Base Models

### CoreModel

For system-level models (User, Permission, Files, etc.):

```python
class CoreModel(models.Model):
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['-id']
        abstract = True
```

### DataCoreModel

For business data models — adds `project` field for isolation:

```python
class DataCoreModel(models.Model):
    project = models.CharField(max_length=255, default='bomiot')
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['-id']
        abstract = True
```

## JSON Data Field Pattern

All business models use `data = JSONField()`:

```python
class Goods(DataCoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_goods'
```

**Advantages:**
- No migrations needed when adding fields
- Flexible schema per project
- Query via `data__field` syntax: `Goods.objects.filter(data__code='SKU001')`

## Model List

| Model | Base | Table |
|-------|------|-------|
| User | CoreModel + AbstractUser | bomiot_user |
| Permission | CoreModel | bomiot_permission |
| Team | DataCoreModel | bomiot_team |
| Goods | DataCoreModel | bomiot_goods |
| Bin | DataCoreModel | bomiot_bin |
| Stock | DataCoreModel | bomiot_stock |
| StockBin | DataCoreModel | bomiot_stock_bin |
| Supplier | DataCoreModel | bomiot_supplier |
| Customer | DataCoreModel | bomiot_customer |
| ASN | DataCoreModel | bomiot_asn |
| ASNDetail | DataCoreModel | bomiot_asn_detail |
| DN | DataCoreModel | bomiot_dn |
| DNDetail | DataCoreModel | bomiot_dn_detail |
| Purchase | DataCoreModel | bomiot_purchase |

## Query Filtering

### Project Isolation

```python
project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
# All queries include project filter
query_data['project'] = project_name
```

### Department Isolation

```python
if self.request.auth.department == 0:
    # Superuser: see all departments
    department_condition = {"data__department__gte": 0}
else:
    # Normal user: see own department and below
    department_condition = {"data__department__gte": self.request.auth.department}
```

### Soft Delete

```python
# Always filter out deleted records
query_data['is_delete'] = False
# Delete = set is_delete=True (not actual DELETE)
db_data.update(is_delete=True, updated_time=timezone.now())
```

### Combined Query Example

```python
Q(**{key: value, **department_condition, "is_delete": False, "project": project_name})
```

## db_table Naming

All tables use `settings.BASE_DB_TABLE` prefix:

```python
db_table = settings.BASE_DB_TABLE + '_goods'
# Result: bomiot_goods
```

This allows multiple bomiot instances in the same database with different `BASE_DB_TABLE` values.
