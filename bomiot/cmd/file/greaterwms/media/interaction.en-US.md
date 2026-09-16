# Front-end and Back-end Interaction

## Introduction

- **Bomiot**'s front-end and back-end interaction uses a unified JSON format, including a redefined query mechanism.
- This completely unifies the front-end and back-end code rules for more efficient development.

---

## Get Data

- Front-end GET request example:

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

- In the URL, `params` concatenates a set of JSON query data.
- The back-end directly executes this JSON and queries the database.

---

## Request Headers

Each request should carry the following headers to complete identity and context authentication.

| Header
| --- | --- |
| `token` | JWT token for user authentication
| `language` | Current language, e.g. `en-US`, `zh-CN`
| `project` | Current project identifier
