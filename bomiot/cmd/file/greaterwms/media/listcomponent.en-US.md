# List Component Development

## Overview

Most business lists (ASN, DN, Stock, User) use a unified **q-table pattern**. Example: `components/inbound/ASNList.vue`.

## Standard Structure

```vue
<template>
  <div class="q-pa-md">
    <q-table
      :rows="rows"
      :columns="columns"
      row-key="index"
      v-model:pagination="pagination"
      @request="onRequest"
    >
      <!-- toolbar -->
      <template v-slot:top="props">
        <q-btn-group flat>
          <q-btn :label="t('refresh')" icon="refresh" @click="onRequest()" />
          <q-btn :label="t('new')" icon="add" @click="createData()" />
        </q-btn-group>
        <q-space />
        <q-input dense v-model="search" @update:model-value="onRequest()" />
      </template>

      <!-- row actions -->
      <template v-slot:body-cell="props">
        <q-td :props="props">
          <q-btn icon="edit" @click="editData(props.rowIndex)" />
        </q-td>
      </template>
    </q-table>
  </div>
</template>
```

## Key Elements

### Columns

```js
const columns = [
  { name: 'index', label: '#', field: 'index' },
  { name: 'asn_code', label: t('asn.code'), field: 'asn_code' },
  { name: 'action', label: t('action'), field: 'action' },
]
```

### Pagination & Request

`@request` fires on pagination/sort/search changes:

```js
function onRequest(props) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination
  get({
    url: 'asn/list/',
    params: { page, limit: rowsPerPage, sortBy, descending, search: search.value }
  }).then(res => {
    rows.value = res.list
    pagination.value.rowsNumber = res.total
  })
}
```

### Search

Search box uses `debounce="300"`:

```html
<q-input dense debounce="300" v-model="search" @update:model-value="onRequest()" />
```

### Pagination Options

```html
:rows-per-page-options="[30, 50, 200, 1000]"
```

## Pattern Summary

| Feature | Implementation |
|---------|---------------|
| Data display | q-table + rows/columns |
| Pagination | v-model:pagination + @request |
| Search | q-input + debounce + onRequest |
| Create | createData() -> dialog |
| Edit | editData(rowIndex) -> dialog |
| Refresh | onRequest() |
