# 状态管理（Pinia Stores）

## 概述

使用 **Pinia** 管理全局状态，所有 store 在 `src/stores/` 目录。部分 store 通过 `persist: { enable: true }` 持久化到 LocalStorage（依赖 `pinia-plugin-persistedstate`）。

## Store 清单

| Store | 作用 | 持久化 |
|-------|------|--------|
| menu | 当前选中的菜单项 | 否 |
| tab | 当前激活的 Tab | 是 |
| token | JWT、用户信息、权限校验 | 是 |
| permission | 用户权限列表 | 是 |
| mdDocs | Markdown 内容与文档名 | 否 |
| dark | 暗黑模式 | 是 |
| language | 当前语言 | 是 |
| project | 当前项目 | 是 |
| leftDrawer | 左侧抽屉开关 | 是 |
| rightDrawer | 右侧抽屉开关 | 是 |

## 如何使用 Store

```js
import { useTokenStore } from 'stores/token'

const tokenStore = useTokenStore()

// 读取状态
console.log(tokenStore.token)

// 调用 action
tokenStore.tokenChange('eyJhbGciOi...')

// 使用 getter
const userinfo = tokenStore.tokenDataGet
```

## tokenStore 详解

`tokenStore` 是核心 store，负责：

### 存储 JWT

```js
tokenStore.tokenChange(res.token)
```

### 解析用户信息（getter）

JWT 的 payload 经 base64 解码后包含用户信息和 `permission` 字段：

```js
tokenDataGet(state) {
  let strings = state.token.split(".")
  var userinfo = JSON.parse(decodeURIComponent(escape(window.atob(strings[1]...))))
  return userinfo
}
```

### 权限校验

```js
tokenStore.userPermissionGet('asn_create')
// 返回 true/false，表示当前用户是否有该权限
```

### Token 过期检查

```js
tokenStore.tokenCheck()
// 比较 exp 与当前时间，过期则清空 token
```

## menuStore 与 tabStore 联动

- `tabStore.tabData` 存储当前 Tab 名
- `MenuLink` 组件 watch `tabStore.tabData`，Tab 切换时自动跳转到该 Tab 的第一个菜单项
- `menuStore.menuData` 存储当前选中的菜单项（包含 tab、title、icon、link、routerTo）

## mdDocsStore 与 MDParser

`mdDocsStore.docName` 变化时，`MDParser` 组件自动请求 `md/<docName>.<lang>.md` 并渲染。
