# Event Bus

## Location

`src/boot/bus.js`

## Implementation

Based on **mitt**, 4 lines:

```js
import mitt from 'mitt'
const emitter = mitt()
export default emitter
```

## Usage

```js
import emitter from 'boot/bus'

emitter.emit('eventName', payload)
emitter.on('eventName', (payload) => { ... })
emitter.off('eventName', handler)
```

## Core Event: needLogin

### Trigger

axios response interceptor fires when `response.data.login` exists:

```js
if (response.data.login) {
  emitter.emit('needLogin', true)
} else {
  emitter.emit('needLogin', false)
}
```

### Listener

MainLayout listens in `onMounted`:

```js
emitter.on('needLogin', (payload) => {
  if (payload) tokenStore.tokenChange('')
})
```

Unsubscribe on unmount:

```js
onBeforeUnmount(() => {
  emitter.off('needLogin')
})
```

## Pinia vs Event Bus

| Scenario | Use |
|----------|-----|
| Shared state (token, menu, tab) | Pinia store |
| One-time notifications (login expiry) | Event bus |
