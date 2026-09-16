# 列表组件开发

## 概述

项目中大量业务列表（ASN、DN、Stock、User 等）采用统一的 **q-table 列表模式**。以 `components/inbound/ASNList.vue` 为例讲解。

## 标准结构

一个列表组件通常包含：

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
      <!-- 顶部工具栏 -->
      <template v-slot:top="props">
        <q-btn-group flat>
          <q-btn :label="t('refresh')" icon="refresh" @click="onRequest()" />
          <q-btn :label="t('new')" icon="add" @click="createData()" />
        </q-btn-group>
        <q-space />
        <q-input dense v-model="search" @update:model-value="onRequest()" />
      </template>

      <!-- 行操作 -->
      <template v-slot:body-cell="props">
        <q-td :props="props">
          <q-btn icon="edit" @click="editData(props.rowIndex)" />
        </q-td>
      </template>
    </q-table>
  </div>
</template>
```

## 核心要素

### 1. 数据列定义（columns）

```js
const columns = [
  { name: 'index', label: '#', field: 'index', align: 'left' },
  { name: 'asn_code', label: t('asn.code'), field: 'asn_code' },
  { name: 'action', label: t('action'), field: 'action' },
]
```

### 2. 分页与请求（onRequest）

`@request` 在分页、排序、搜索变化时触发：

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

### 3. 搜索

搜索框使用 `debounce="300"` 防抖，输入变化触发 `onRequest`：

```html
<q-input dense debounce="300" v-model="search" @update:model-value="onRequest()" />
```

### 4. 行操作

通过 `body-cell` 插槽自定义操作列：

```html
<q-btn icon="edit" @click="editData(props.rowIndex)" />
```

## 分页配置

```html
:rows-per-page-options="[30, 50, 200, 1000]"
```

## 通用模式总结

| 功能 | 实现方式 |
|------|----------|
| 数据展示 | q-table + rows/columns |
| 分页 | v-model:pagination + @request |
| 搜索 | q-input + debounce + onRequest |
| 新增 | createData() → 表单对话框 |
| 编辑 | editData(rowIndex) → 表单对话框 |
| 刷新 | onRequest() |
