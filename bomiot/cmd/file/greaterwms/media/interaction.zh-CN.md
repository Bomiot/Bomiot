# 前后端交互

## 介绍

- **Bomiot** 的前后端交互使用统一的 JSON 格式，包括重新定义的查询机制。
- 这样可以完全统一前后端代码规则，并更高效地开发。

---

## 获取数据

- 前端 GET 请求示例：

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

- 在 URL 中，`params` 拼接了一组 JSON 查询数据。
- 后端会直接执行这个 JSON，然后查询数据库。

---

## 请求头

每个请求都应携带以下请求头，以完成身份和上下文认证。

| 头
| `token` | 用于用户认证的 JWT token
| `language` | 当前语言，如 `en-US`、`zh-CN`
| `project` | 当前项目标识
