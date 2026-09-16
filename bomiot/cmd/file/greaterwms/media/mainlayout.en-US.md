# MainLayout.vue

## Location

`src/layouts/MainLayout.vue`

## Structure

MainLayout is the shell for all business pages, using Quasar's `q-layout`:

```html
<q-layout view="hHh LpR fFf">
  <q-header>              <!-- top bar -->
  <q-drawer side="left">  <!-- left menu -->
  <q-drawer side="right"> <!-- right drawer -->
  <q-page-container>      <!-- page content -->
    <router-view />
  </q-page-container>
</q-layout>
```

### view attribute

`view="hHh LpR fFf"` - three groups control header/middle/footer:

- `L` (uppercase) = left drawer **fixed**, does not scroll with page
- `p` = page area scrollable
- `R` (uppercase) = right drawer fixed

## Header (q-header)

Contains:
1. **Menu button**: toggle left drawer
2. **Logo + app name**: click to go home `/`
3. **Project selector**: switch project, writes cookie and reloads
4. **External links**: Bilibili, YouTube, Gitee, GitHub
5. **Language selector** (LangChoice)
6. **Dark mode** (DarkMode)
7. **Login/Logout button**: shown based on tokenStore.token

## Left Drawer

```html
<q-drawer v-model="leftDrawerStore.leftDrawerOpen" side="left" :breakpoint="500">
  <q-list dense padding>
    <MenuLink />
  </q-list>
</q-drawer>
```

`breakpoint="500"`: switches to overlay drawer below 500px width.

## Login Flow

1. Click "Login" -> `loginForm = true` opens dialog
2. Enter credentials -> `submitLogin()`
3. Call `post('login/', loginData.value)`
4. On success: `tokenStore.tokenChange(res.token)`, emit `needLogin` false

```js
async function submitLogin () {
  await post('login/', loginData.value).then((res) => {
    if (!res.login) {
      tokenStore.tokenChange(res.token)
      emitter.emit('needLogin', false)
      cancelLogin()
    }
  })
}
```

## Lifecycle

### onMounted

```js
onMounted(() => {
  tokenStore.tokenCheck()   // check if token expired
  listenToEvent()            // listen to needLogin
  getProjectList()           // load project list
})
```

### needLogin Event

When backend returns login expired, clear token:

```js
emitter.on('needLogin', (payload) => {
  if (payload) tokenStore.tokenChange('')
})
```
