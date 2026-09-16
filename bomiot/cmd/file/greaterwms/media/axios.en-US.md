# axios.js

## Location

`src/boot/axios.js`

## Architecture

1. Create axios instance
2. Configure request/response interceptors
3. Export wrapped methods (get/post/put/patch/delete/fileUpload)

## Request Throttling

`SimpleThrottler` enforces minimum 250ms between requests:

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

## Request Interceptor

```js
api.interceptors.request.use((config) => {
  // 1. token from LocalStorage
  config.headers.token = token
  // 2. language
  config.headers.language = lang  // zh-CN or en-US
  // 3. project
  config.headers.project = project  // greaterwms
  // 4. show loading
  Loading.show()
  return config
})
```

No token + not login request -> warn and reject.

## Response Interceptor

```js
api.interceptors.response.use((response) => {
  if (response.data.detail) Notify.warning(detail)
  if (response.data.msg)    Notify.success(msg)
  if (response.data.login)  emitter.emit('needLogin', true)
  Loading.hide()
  return response.data   // returns data directly
})
```

Note: returns `response.data` directly, so business code gets the data body.

## Exported Methods

```js
get({ url, params })
post(url, data)
put(url, data)
patch(url, data)
deleteData(url)
fileUpload(url, formData, onProgress)
```

## Usage

```js
import { get, post } from 'boot/axios'

get({ url: 'asn/list/', params: { page: 1 } }).then(res => { ... })
post('login/', { username, password }).then(res => { ... })
```

## File Upload

```js
fileUpload('upload/', formData, (percent) => {
  console.log(`${percent}%`)
})
```
