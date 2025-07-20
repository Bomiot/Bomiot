# Structure

## 介绍

- **Bomiot** 支持Django, FastAPI, Flask，所以Django的ORM是通用的，并且支持异步

---

## 用户

```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

- 获取用户models，然后使用这个User来对用户进行增删改查

---

## Team

- 每个用户都需要绑定一个team
- team是以组的概念，对用户的权限进行管理
- 当team的权限发生变化时，User的权限也同时发生改变
- team不对用户数据进行隔离

---

## Department

- 每个用户都需要绑定一个department
- department是以数据组的概念，对用户数据进行隔离
- User只能看到自己department的数据

---

## Data

- **Bomiot** 认为，前端传给后端是一组标准Json数据，而后端却还需要对Json的每个字段进行逐个编写，这大大降低工作效率
- Data类的Models，只有1个JSONField,Django的JSONField已经综合了各种查询读写，非常全面
- 数据的存取交由**Bomiot**的信号进行处理
- 这样就可以前后端代码一致，比如`data__value__gte=1`
- 仅需要确定前端的数据Json字段，即可完成数据管理