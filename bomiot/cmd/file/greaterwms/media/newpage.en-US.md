# How to Add a New Page

## Steps

### 1. Create Page Component

Create `.vue` in `src/pages/`. Example: supplier page.

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

### 2. Register Route

Add to `src/router/routes.js` children:

```js
{ path: 'supplier', component: () => import('pages/base/SupplierReader.vue') },
```

**Note**: Do NOT set `meta` field (guard compatibility issue).

### 3. Add Menu Item

Add to `src/components/MenuLink.vue`:

```js
{ tab: 'standard', title: t('supplier.name'), icon: 'contact_mail', link: '/supplier' },
```

### 4. Add i18n

`src/i18n/zh-CN/index.js` and `en-US/index.js`:

```js
// zh-CN
supplier: { name: '供应商' }
// en-US
supplier: { name: 'Supplier' }
```

### 5. Build

```bash
quasar build
```

## Page Template

All Reader pages use:

```vue
<template>
  <q-page class="flex flex-top">
    <YourListComponent />
  </q-page>
</template>
```

## Checklist

- [ ] Page in `src/pages/` subdirectory
- [ ] Route in `routes.js`, no `meta`
- [ ] Menu item in `MenuLink.vue`
- [ ] i18n translations (zh-CN + en-US)
- [ ] `quasar build` passes
