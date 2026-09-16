# 前端开发

## 简介

Bomiot 内置一套基于 **Quasar + Vue 3** 的前端模板，同时兼容 React 与 Angular。官方推荐使用 Quasar + Vue 3 以获得最完整的开箱即用能力（含布局、组件、国际化、请求封装等）。

---

## 技术栈

- **框架**：Vue 3 + Quasar
- **构建**：Vite（Quasar CLI）
- **状态管理**：Pinia
- **路由**：Vue Router
- **国际化**：vue-i18n
- **HTTP 客户端**：Axios（统一封装）

---

## 目录结构

```
templates/                 # 前端根目录
├── src/
│   ├── assets/            # 静态资源
│   ├── boot/              # 启动脚本（axios、i18n 等）
│   ├── components/        # 通用组件
│   ├── layouts/           # 布局组件
│   ├── pages/             # 页面组件
│   ├── router/            # 路由配置
│   ├── stores/            # Pinia 状态
│   ├── i18n/              # 多语言文件
│   └── App.vue
├── statics/               # 图标等静态文件
├── quasar.config.js       # Quasar 配置
└── package.json
```

---

## 安装依赖

```bash
cd templates

yarn install
# 或
npm install
```

---

## 配置后端地址

编辑 `src/boot/axios.js`，设置后端 API 地址：

```js
const baseURL = 'http://127.0.0.1:8000'
const api = axios.create({ baseURL })
```

默认后端运行在 `http://127.0.0.1:8000`。

---

## 开发模式

```bash
# 确保后端已启动
bomiot run

# 启动前端开发服务器（热更新）
quasar dev
```

---

## 生产构建

```bash
# 构建产物输出到 templates/dist/spa/
quasar build
```

> 注意：Django 后端服务的是 `templates/dist/spa/` 目录下的产物，因此修改前端后必须执行 `quasar build` 才能生效。

---

## 请求封装

所有 API 请求统一通过 `src/boot/axios.js` 封装，导出 `get`、`post`、`put`、`patch`、`deleteData` 等方法。

请求头自动携带：
- `token`：JWT 认证令牌
- `language`：当前语言（如 `zh-CN`）
- `project`：项目标识（如 `bomiot`）

```js
import { get, post } from 'boot/axios'

// GET 请求
const res = await get({ url: 'core/user/', params: { page: 1, max_page: 20 } })

// POST 请求
const res = await post({ url: 'core/user/create/', body: { username: 'admin' } })
```

---

## 页面与路由

页面放在 `src/pages/` 下，路由在 `src/router/routes.js` 中注册：

```js
{ path: 'my-page', component: () => import('pages/MyPage.vue') }
```

---

## 国际化

语言文件位于 `src/i18n/`，支持 `zh-CN` 和 `en-US`。组件中使用 `useI18n`：

```js
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
```

---

## 菜单与 Tab

- **Tab 栏**：`src/components/TabList.vue` 定义顶部 Tab
- **菜单**：`src/components/MenuLink.vue` 定义左侧菜单，通过 `tab` 字段归属到对应 Tab

---

## 文档页面

文档页面通过 `MDParser` 组件渲染 Markdown，文档源文件存放在后端 `greaterwms/media/` 目录，由 `md/<docName>.<lang>.md` 接口提供。
