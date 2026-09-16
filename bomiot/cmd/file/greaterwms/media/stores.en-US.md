# Pinia Stores

## Overview

Uses **Pinia** for state management. Stores in `src/stores/`. Some persist to LocalStorage via `persist: { enable: true }` (`pinia-plugin-persistedstate`).

## Store List

| Store | Purpose | Persisted |
|-------|---------|-----------|
| menu | Current menu item | No |
| tab | Current active tab | Yes |
| token | JWT, user info, permission | Yes |
| permission | Permission list | Yes |
| mdDocs | Markdown content & doc name | No |
| dark | Dark mode | Yes |
| language | Current language | Yes |
| project | Current project | Yes |
| leftDrawer | Left drawer state | Yes |
| rightDrawer | Right drawer state | Yes |

## Usage

```js
import { useTokenStore } from 'stores/token'
const tokenStore = useTokenStore()

console.log(tokenStore.token)           // read state
tokenStore.tokenChange('eyJ...')        // call action
const userinfo = tokenStore.tokenDataGet // use getter
```

## tokenStore

### Store JWT

```js
tokenStore.tokenChange(res.token)
```

### Parse User Info (getter)

JWT payload decoded via base64 contains user info and `permission`:

```js
tokenDataGet(state) {
  let strings = state.token.split(".")
  var userinfo = JSON.parse(decodeURIComponent(escape(window.atob(strings[1]...))))
  return userinfo
}
```

### Permission Check

```js
tokenStore.userPermissionGet('asn_create')  // true/false
```

### Token Expiry

```js
tokenStore.tokenCheck()  // clears token if expired
```

## menuStore & tabStore

- `tabStore.tabData`: current tab name
- `MenuLink` watches `tabStore.tabData`, auto-navigates to first item of that tab
- `menuStore.menuData`: current selected menu item (tab, title, icon, link, routerTo)
