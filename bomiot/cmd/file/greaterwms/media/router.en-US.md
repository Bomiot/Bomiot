# Router System

## Structure

```
src/router/
├── routes.js    # route table
└── index.js     # Router instance + guard
```

## Route Table (routes.js)

All routes are children of `MainLayout`:

```js
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'asnlist', component: () => import('pages/inbound/ASNReader.vue') },
    ]
  },
  { path: '/404', component: () => import('pages/ErrorNotFound.vue') },
  { path: '/:catchAll(.*)*', component: () => import('pages/ErrorNotFound.vue') }
]
```

Mode set by `quasar.config.js` `build.vueRouterMode`, currently `hash`.

## Global Guard (index.js)

```js
Router.beforeEach((to, from, next) => {
  if (to.meta) {
    next(vm => { vm.$router.replace(to.path) })
  } else {
    next()
  }
})
```

**Important**: This guard uses Vue Router 3 syntax. Routes with `meta` trigger the broken branch. **Do NOT set `meta` on new routes**.

## Naming Convention

- Business pages: `/<module>`, e.g. `/asnlist`, `/stock`
- Dev docs: `/dev-<docName>`, e.g. `/dev-axios`

## Dev Doc Routes

All `/dev-*` routes reuse `DevReader.vue`:

```js
{ path: 'dev-axios', component: () => import('pages/dev/DevReader.vue') },
```

`DevReader.vue` derives `docName` from `route.path`:

```js
const name = route.path.replace(/^\/dev-/, '')  // /dev-axios -> axios
```

Since Vue Router reuses the component, `onMounted` runs once. Use `watch(() => route.path, updateDocName)` to handle changes.
