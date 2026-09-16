# axios.js 运作机制

## 文件位置

`src/boot/axios.js`

## 整体架构

axios.js 做了三件事：
1. 创建 axios 实例
2. 配置请求/响应拦截器
3. 导出封装好的请求方法（get/post/put/patch/delete/fileUpload）

## 请求节流

内置 `SimpleThrottler`，强制请求间隔至少 250ms：

```js
class SimpleThrottler {
  constructor(interval = 250) { ... }
  async throttle() {
    const now = Date.now()
    if (now - this.lastRequestTime < this.interval) {
      await new Promise(r => setTimeout(r, this.interval - (now - this.lastRequestTime)))
    }
    this.lastRequestTime = Date.now()
  }
}
```

每个请求方法都被 `throttledRequest` 包装，先等待节流再发起。

## 请求拦截器

每次请求发出前执行：

```js
api.interceptors.request.use((config) => {
  // 1. 读取 token，设置请求头
  let token = ''
  if (LocalStorage.has('token')) {
    token = JSON.parse(LocalStorage.getItem('token')).token
  }
  config.headers.token = token

  // 2. 读取语言
  config.headers.language = lang  // zh-CN 或 en-US

  // 3. 读取项目
  config.headers.project = project  // greaterwms

  // 4. 显示加载
  Loading.show()
  return config
})
```

无 token 且非登录请求时，弹出 `Please Login First` 并拒绝请求。

## 响应拦截器

响应返回后执行：

```js
api.interceptors.response.use((response) => {
  if (response.data.detail) Notify.create({ type: 'warning', message: response.data.detail })
  if (response.data.msg)    Notify.create({ type: 'success', message: response.data.msg })
  if (response.data.login)  emitter.emit('needLogin', true)
  else                      emitter.emit('needLogin', false)
  Loading.hide()
  return response.data   // 直接返回 data，不用再写 res.data
})
```

注意：拦截器直接返回 `response.data`，所以业务代码拿到的就是后端返回的数据体。

## 导出的请求方法

```js
async function get({ url, params }) { ... }
async function post(url, data) { ... }
async function put(url, data) { ... }
async function patch(url, data) { ... }
async function deleteData(url) { ... }
async function fileUpload(url, formData, onProgress) { ... }
```

## 使用示例

```js
import { get, post } from 'boot/axios'

// GET
get({ url: 'asn/list/', params: { page: 1 } }).then(res => {
  // res 就是后端返回的数据
})

// POST
post('login/', { username: 'admin', password: '123' }).then(res => {
  // res.token 是 JWT
})
```

## 文件上传

`fileUpload` 支持进度回调：

```js
fileUpload('upload/', formData, (percent) => {
  console.log(`上传进度: ${percent}%`)
})
```
