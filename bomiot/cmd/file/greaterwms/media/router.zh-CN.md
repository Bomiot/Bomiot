# 路由系统

## 文件结构

```
src/router/
├── routes.js    # 路由表
└── index.js     # Router 实例 + 全局守卫
```

## 路由表（routes.js）

所有业务路由作为 `MainLayout` 的 children 挂载，共享布局壳：

```js
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'asnlist', component: () => import('pages/inbound/ASNReader.vue') },
      // ...
    ]
  },
  { path: '/404', component: () => import('pages/ErrorNotFound.vue') },
  { path: '/:catchAll(.*)*', component: () => import('pages/ErrorNotFound.vue') }
]
```

路由模式由 `quasar.config.js` 的 `build.vueRouterMode` 决定，当前为 `hash`。

## 全局守卫（index.js）

```js
Router.beforeEach((to, from, next) => {
  if (to.meta) {
    next(vm => { vm.$router.replace(to.path) })
  } else {
    next()
  }
})
```

**重要**：此守卫使用 Vue Router 3 的写法。带 `meta` 的路由会走 `if` 分支，导致导航异常。因此**新增路由不要设置 `meta` 字段**。

## 路由命名约定

- 业务页面：`/<module>`，如 `/asnlist`、`/stock`
- 开发文档：`/dev-<docName>`，如 `/dev-axios`

## 开发文档路由的特殊处理

所有 `/dev-*` 路由复用同一个 `DevReader.vue`：

```js
{ path: 'dev-axios', component: () => import('pages/dev/DevReader.vue') },
{ path: 'dev-router', component: () => import('pages/dev/DevReader.vue') },
```

`DevReader.vue` 从 `route.path` 推导 `docName`：

```js
const name = route.path.replace(/^\/dev-/, '')  // /dev-axios -> axios
mdDataStore.docNameChange(name)
```

由于 Vue Router 复用相同组件，`onMounted` 只执行一次，所以用 `watch(() => route.path, updateDocName)` 监听路由变化。
