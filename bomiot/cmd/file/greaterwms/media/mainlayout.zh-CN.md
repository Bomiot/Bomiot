# MainLayout.vue 运作机制

## 文件位置

`src/layouts/MainLayout.vue`

## 整体结构

MainLayout 是所有业务页面的布局壳，使用 Quasar 的 `q-layout` 构建三栏式布局：

```html
<q-layout view="hHh LpR fFf">
  <q-header>    <!-- 顶部栏 -->
  <q-drawer side="left">   <!-- 左侧菜单 -->
  <q-drawer side="right">  <!-- 右侧抽屉 -->
  <q-page-container>       <!-- 页面内容区 -->
    <router-view />
  </q-page-container>
</q-layout>
```

### view 属性解析

`view="hHh LpR fFf"` 三组字符分别控制 头部/中间/底部 的布局：

- `L`（大写）= 左侧抽屉**固定**，不随页面滚动
- `p` = 页面区域可滚动
- `R`（大写）= 右侧抽屉固定

## 顶部栏（q-header）

包含以下元素：

1. **菜单按钮**：控制左侧抽屉开关（`leftDrawerStore.toggleleftDrawer`）
2. **Logo + 应用名**：点击跳转到首页 `/`
3. **项目选择器**（q-select）：切换项目，选择后写入 cookie 并刷新页面
4. **外链按钮**：Bilibili、YouTube、Gitee、GitHub
5. **语言选择**（LangChoice 组件）
6. **暗黑模式**（DarkMode 组件）
7. **登录/登出按钮**：根据 tokenStore.token 是否为空切换显示

## 左侧菜单（q-drawer）

```html
<q-drawer v-model="leftDrawerStore.leftDrawerOpen" side="left" :breakpoint="500">
  <q-list dense padding>
    <MenuLink />
  </q-list>
</q-drawer>
```

- `breakpoint="500"`：窗口宽度小于 500px 时自动切换为覆盖式抽屉
- 菜单项由 `MenuLink` 组件渲染

## 登录流程

1. 点击「登录」按钮 → `loginForm = true` 弹出登录对话框
2. 输入用户名密码 → `submitLogin()`
3. 调用 `post('login/', loginData.value)`
4. 成功后 `tokenStore.tokenChange(res.token)` 存储 JWT
5. 发出 `needLogin` 事件为 false

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

## 登出

```js
function logOuts () {
  tokenStore.tokenChange('')
}
```

清空 tokenStore 中的 JWT。

## 生命周期

### onMounted

```js
onMounted(() => {
  tokenStore.tokenCheck()   // 检查 token 是否过期
  listenToEvent()            // 监听 needLogin 事件
  getProjectList()           // 获取项目列表
})
```

### 事件监听

监听 event bus 的 `needLogin` 事件，当后端返回登录失效时清空 token：

```js
emitter.on('needLogin', (payload) => {
  if (payload) {
    tokenStore.tokenChange('')
  }
})
```

## 项目切换

选择项目后写入 cookie 并刷新页面：

```js
watch(() => projectStore.project, val => {
  if (val) {
    $q.cookies.set('project', val)
    window.location.reload(true)
  }
})
```
