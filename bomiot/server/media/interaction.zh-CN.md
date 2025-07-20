# 前后端交互

## 介绍

- **Bomiot** 的前后端交互是统一的一个Json，包括查询也做了重新定义
- 这样可以完全统一前后端代码规则，并更高效的开发

---

## 获取数据

- 前端
```js
get({
    url: 'core/example/',
    params: {
      params: JSON.stringify({ data__value__icontains: search.value }),
      page: requestData.pagination.page,
      max_page: requestData.pagination.rowsPerPage
    }
  })
```

- 在url中，params拼接了一个params，这个params是一组json查询数据
- 后端会直接执行这个json，然后进行数据库查询