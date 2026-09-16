# quasar.config.js

## Location

`greaterwms/templates/quasar.config.js`

## Structure

```js
export default defineConfig((ctx) => {
  return {
    boot: [...],
    css: [...],
    extras: [...],
    build: {...},
    devServer: {...},
    framework: {...},
    animations: [...],
  }
})
```

## boot Files

```js
boot: ['axios', 'i18n', 'notify-defaults', 'pinia']
```

Execution order: axios, i18n, notify-defaults, pinia.

## css

```js
css: ['app.scss', 'app.sass']
```

## extras

```js
extras: ['mdi-v7', 'roboto-font', 'material-icons']
```

- `mdi-v7`: Material Design Icons
- `roboto-font`: Roboto font
- `material-icons`: Material Icons

## build

```js
build: {
  target: { browser: ['es2022', ...], node: 'node18' },
  vueRouterMode: 'hash',
  vitePlugins: [
    ['@intlify/unplugin-vue-i18n/vite', { include: ['./src/i18n'] }],
    ['vite-plugin-checker', { eslint: {...} }, { server: false }]
  ]
}
```

- `vueRouterMode: 'hash'`: hash routing (URL with `#`)

## devServer

```js
devServer: { open: true }
```

## framework

```js
framework: {
  plugins: ['Dialog', 'Loading', 'Meta', 'LocalStorage', 'Cookies', 'Notify']
}
```

## animations

```js
animations: ['fadeIn', 'fadeOut']
```
