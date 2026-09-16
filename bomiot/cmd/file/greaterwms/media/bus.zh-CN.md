# 事件总线（Event Bus）

## 文件位置

`src/boot/bus.js`

## 实现

基于 **mitt** 库，仅 4 行代码：

```js
import mitt from 'mitt'
const emitter = mitt()
export default emitter
```

## 使用方式

```js
import emitter from 'boot/bus'

// 发送事件
emitter.emit('eventName', payload)

// 监听事件
emitter.on('eventName', (payload) => { ... })

// 取消监听
emitter.off('eventName', handler)
```

## 核心事件：needLogin

### 触发时机

axios 响应拦截器检测到后端返回 `response.data.login` 时触发：

```js
// axios.js
if (response.data.login) {
  emitter.emit('needLogin', true)
} else {
  emitter.emit('needLogin', false)
}
```

### 监听方

MainLayout.vue 在 `onMounted` 中监听：

```js
function listenToEvent() {
  emitter.on('needLogin', (payload) => {
    if (payload) {
      tokenStore.tokenChange('')  // 清空 token
    }
  })
}
```

组件卸载时取消监听：

```js
onBeforeUnmount(() => {
  emitter.off('needLogin')
})
```

## 与 Pinia 的分工

| 场景 | 用什么 |
|------|--------|
| 跨组件共享状态（token、菜单、Tab） | Pinia store |
| 跨组件触发一次性通知（登录失效、刷新列表） | Event bus |
