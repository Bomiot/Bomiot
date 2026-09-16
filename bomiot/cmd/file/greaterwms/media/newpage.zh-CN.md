# 如何新增一个页面

## 步骤

### 1. 创建页面组件

在 `src/pages/` 下创建 `.vue` 文件。例如创建一个供应商页面：

```vue
<!-- src/pages/base/SupplierReader.vue -->
<template>
  <q-page class="flex flex-top">
    <SupplierList />
  </q-page>
</template>

<script setup>
import SupplierList from 'components/base/SupplierList.vue'
</script>
```

Reader 页面是轻量容器，内部引入业务组件。

### 2. 注册路由

在 `src/router/routes.js` 的 `children` 数组中添加：

```js
{ path: 'supplier', component: () => import('pages/base/SupplierReader.vue') },
```

**注意**：不要设置 `meta` 字段（路由守卫兼容问题）。

### 3. 添加菜单项

在 `src/components/MenuLink.vue` 的 `menuLinks` 数组中添加：

```js
{ tab: 'standard', title: t('supplier.name'), icon: 'contact_mail', link: '/supplier' },
```

### 4. 添加国际化

在 `src/i18n/zh-CN/index.js` 和 `en-US/index.js` 中添加翻译：

```js
// zh-CN
supplier: { name: '供应商' }
// en-US
supplier: { name: 'Supplier' }
```

### 5. 构建

```bash
quasar build
```

## 页面模板规范

所有 Reader 页面使用统一模板：

```vue
<template>
  <q-page class="flex flex-top">
    <YourListComponent />
  </q-page>
</template>
```

`q-page` 是 Quasar 页面容器，`flex flex-top` 让内容顶部对齐。

## 检查清单

- [ ] 页面组件放在 `src/pages/` 对应子目录
- [ ] 路由注册在 `routes.js`，无 `meta`
- [ ] 菜单项添加到 `MenuLink.vue`
- [ ] 国际化翻译已添加（zh-CN + en-US）
- [ ] 运行 `quasar build` 无报错
