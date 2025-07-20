# Structure

## Introduction

- **Bomiot** is compatible with Django, FastAPI, and Flask. Therefore, Django's ORM is universal and supports asynchronous operations.

---

## User

```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

- Retrieve the user model and utilize this User to perform create, read, update, and delete operations on users.

---

## Team

- Each user must be associated with a team.
- A team, functioning as a group concept, manages user permissions.
- When the permissions of a team change, the permissions of the associated users change simultaneously.
- Teams do not isolate user data.

---

## Department

- Each user must be assigned to a department.
- A department, serving as a data group concept, isolates user data.
- Users can only view data from their own department.

---

## Data

- **Bomiot** recognizes that while the frontend sends a standard JSON data set to the backend, developers still have to individually code each field of the JSON on the backend, which significantly reduces work efficiency.
- Data class models have only one JSONField. Django's JSONField already integrates various query, read, and write capabilities, making it highly comprehensive.
- Data storage and retrieval are handled by **Bomiot** signals.
- This enables consistent code between the frontend and backend. For example, `data__value__gte=1`.
- Data management can be completed simply by defining the JSON fields of the frontend data.