# Department Isolation

## Overview

bomiot backend isolates data by `department` field. Users can only see data from their own department and sub-departments, not from higher-level departments.

> Note: bomiot's `CorePermission.has_permission` simply `return True` — there is **no permission management**. Data isolation is achieved solely through `get_queryset` department filtering.

## 1. User Model

`bomiot/server/core/models.py`:

```python
class User(AbstractUser, CoreModel):
    department = models.IntegerField(default=0)  # 0 = superuser
```

- `department = 0`: superuser, sees all departments
- `department = N` (N > 0): normal user, sees only `department >= N`

## 2. Department Isolation in get_queryset

`bomiot/server/core/handler.py` (`ExampleList.get_queryset`) and `bomiot/server/function/goods.py` (`GoodsList.get_queryset`):

```python
def get_queryset(self):
    project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    # ... parse query params ...

    if not any(key.startswith('data__department') for key in query_data):
        query_data = {key: value for key, value in query_data.items()
                      if not key.startswith('data__department')}
        if self.request.auth.department == 0:
            department_condition = {"data__department__gte": 0}
        else:
            department_condition = {"data__department__gte": self.request.auth.department}
    else:
        department_condition = {"data__department__gte": self.request.auth.department}

    # ... build query conditions ...
    or_conditions.append(Q(**{key: value, **department_condition,
                              "is_delete": query_data['is_delete'],
                              "project": project_name}))
    return models.Example.objects.filter(query_conditions).order_by(ordering)
```

### Isolation Rules

| User department | Query condition | Visible range |
|----------------|-----------------|---------------|
| 0 (superuser) | `data__department__gte=0` | All departments |
| 1 | `data__department__gte=1` | Dept 1 and below |
| 2 | `data__department__gte=2` | Dept 2 and below, NOT dept 1 |

### Anti-escalation

Even if a user explicitly passes `data__department` in query params, it still falls back to `__gte=self.request.auth.department`, preventing access to higher-level departments.

## 3. Department Hierarchy

Departments use integers, higher number = lower level:

```
department = 0  → superuser (headquarters)
department = 1  → level-1 department
department = 2  → level-2 department
department = 3  → level-3 department
...
```

- Dept 1 sees depts 1, 2, 3...
- Dept 2 sees only depts 2, 3... (not dept 1)

## 4. Combined with Project Isolation

Every query includes both `project` and `department` filters:

```python
Q(**{key: value,
     **department_condition,           # department isolation
     "is_delete": query_data['is_delete'],  # soft delete
     "project": project_name})               # project isolation
```

Three layers: **project isolation + department isolation + soft delete**.

## 5. Setting User Department

`bomiot/server/core/views.py`:

```python
class UserSetDepartment(viewsets.ModelViewSet):
    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=int(data.get('id')), is_delete=False)
        if user_check.exists():
            user_data = user_check.first()
            user_data.department = int(data.get('department'))
            user_data.save()
        return Response(msg_message_return(language, "Success set department"), status=200)
```

Takes effect immediately — next query uses the new `department` value.
