# Permission & Department Isolation

## Permission Model

```python
class Permission(CoreModel):
    api = models.CharField(max_length=255)    # URL path
    name = models.CharField(max_length=255)    # Human-readable name
```

## Permission Initialization

`init_permission()` in `server/views.py` auto-generates permissions from all registered URLs:

```python
def init_permission():
    Permission.objects.all().delete()
    user_objs = list(User.objects.filter(is_superuser=True))

    all_api_info = list(get_all_url())  # Scans all URL patterns
    for data in all_api_info:
        perm_obj = Permission(api=str(data[0]), name=str(data[1]))
        perm_objs.append(perm_obj)
        for user in user_objs:
            user.permission[str(data[1])] = str(data[0])

    Permission.objects.bulk_create(perm_objs)
    User.objects.bulk_update(user_objs, ['permission'])
```

## Team-Based Permission

### Team Model

```python
class Team(DataCoreModel):
    name = models.CharField(max_length=255)
    permission = models.JSONField(default=dict)  # {"Permission Name": "URL path"}
```

### Assign Permission to Team

```python
class TeamPermission(viewsets.ModelViewSet):
    def create(self, request):
        permission_list = data.get('permission')
        data_list = list(map(lambda data: self.get_permission_data(data), permission_list))
        permission_data = reduce(lambda x, y: {**x, **y}, data_list)
        team_data.permission = permission_data
        # Also update all users in the team
        User.objects.filter(team=team_data.id).update(permission=permission_data)
```

### Set Team for User

```python
class UserSetTeam(viewsets.ModelViewSet):
    def create(self, request):
        team_data = models.Team.objects.filter(id=data.get('team_id')).first()
        user_data.permission = team_data.permission
        user_data.team = int(data.get('team_id'))
```

## Permission Check in ViewSets

```python
if "Create One User" not in self.request.auth.permission:
    raise APIException(detail_message_return(lang, "User does not have permission to create user"))

if "Delete Team" not in self.request.auth.permission:
    raise APIException(detail_message_return(lang, "User does not have permission to delete team"))
```

## Department Isolation

### User Department

```python
class User(AbstractUser, CoreModel):
    department = models.IntegerField(default=0)  # 0 = superuser
```

### Query Filtering

```python
def get_queryset(self):
    if self.request.auth.department == 0:
        # Superuser: see all
        department_condition = {"data__department__gte": 0}
    else:
        # Normal: see own department and sub-departments
        department_condition = {"data__department__gte": self.request.auth.department}

    # Applied to every query
    Q(**{key: value, **department_condition, "is_delete": False, "project": project_name})
```

### Department Hierarchy

- `department = 0`: superuser, sees everything
- `department = 1`: sees department 1, 2, 3, ... (itself and below)
- `department = 2`: sees department 2, 3, ... (not department 1)

## Project Isolation

Combined with department isolation in every query:

```python
project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
# Final filter includes: project=project_name AND department_condition
```

## Three-Layer Isolation

```
1. Project isolation    — project field + HTTP_PROJECT header
2. Department isolation — data__department field + user.department
3. Soft delete          — is_delete=False
```
