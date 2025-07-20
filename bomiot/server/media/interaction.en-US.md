# Front-end and back-end interaction

## Introduction

- **Bomiot**'s front-end and back-end interaction is a unified Json, including the redefinition of queries
- This can completely unify the front-end and back-end code rules and develop more efficiently

---

## Get data

- Front-end
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

- In the url, params is spliced with a params, which is a set of json query data
- The back-end will directly execute this json and then query the database