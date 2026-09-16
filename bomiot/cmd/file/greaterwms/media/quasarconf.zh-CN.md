# quasar.config.js 配置讲解

## 文件位置

`greaterwms/templates/quasar.config.js`

## 配置结构

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
    // ... 其他平台配置
  }
})
```

## boot 启动文件

```js
boot: ['axios', 'i18n', 'notify-defaults', 'pinia']
```

按顺序执行的启动文件：
1. `axios`：HTTP 请求封装
2. `i18n`：国际化初始化
3. `notify-defaults`：通知默认配置
4. `pinia`：状态管理初始化

## css 全局样式

```js
css: ['app.scss', 'app.sass']
```

加载 `src/css/` 下的全局样式文件。

## extras 资源

```js
extras: ['mdi-v7', 'roboto-font', 'material-icons']
```

- `mdi-v7`：Material Design Icons（图标库）
- `roboto-font`：Roboto 字体
- `material-icons`：Material Icons 图标

## build 构建配置

```js
build: {
  target: {
    browser: ['es2022', 'firefox115', 'chrome115', 'safari14'],
    node: 'node18'
  },
  vueRouterMode: 'hash',   // 路由模式：hash
  vitePlugins: [
    ['@intlify/unplugin-vue-i18n/vite', {
      include: [fileURLToPath(new URL('./src/i18n', import.meta.url))]
    }],
    ['vite-plugin-checker', { eslint: {...} }, { server: false }]
  ]
}
```

关键点：
- `vueRouterMode: 'hash'`：使用 hash 路由模式（URL 带 `#`）
- `vitePlugins`：加载 i18n 资源和 ESLint 检查插件

## devServer 开发服务器

```js
devServer: {
  open: true   // 启动后自动打开浏览器
}
```

## framework 框架配置

```js
framework: {
  config: { notify: {} },
  plugins: ['Dialog', 'Loading', 'Meta', 'LocalStorage', 'Cookies', 'Notify']
}
```

注册的 Quasar 插件：
- `Dialog`：对话框
- `Loading`：加载指示器
- `Meta`：页面 meta 信息
- `LocalStorage`：本地存储
- `Cookies`：Cookie 操作
- `Notify`：通知消息

## animations 动画

```js
animations: ['fadeIn', 'fadeOut']
```

只加载用到的动画（fadeIn/fadeOut），减小包体积。
