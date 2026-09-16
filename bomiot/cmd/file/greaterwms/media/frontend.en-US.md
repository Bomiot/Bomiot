# Frontend Development

## Introduction

Bomiot ships with a frontend template based on **Quasar + Vue 3**, while also being compatible with React and Angular. The official recommendation is Quasar + Vue 3 for the most complete out-of-the-box experience (layout, components, i18n, request wrapper, etc.).

---

## Tech Stack

- **Framework**: Vue 3 + Quasar
- **Build**: Vite (Quasar CLI)
- **State**: Pinia
- **Router**: Vue Router
- **i18n**: vue-i18n
- **HTTP**: Axios (unified wrapper)

---

## Directory Structure

```
templates/                 # Frontend root
├── src/
│   ├── assets/            # Static assets
│   ├── boot/              # Boot scripts (axios, i18n, etc.)
│   ├── components/        # Shared components
│   ├── layouts/           # Layout components
│   ├── pages/             # Page components
│   ├── router/            # Route config
│   ├── stores/            # Pinia stores
│   ├── i18n/              # Locale files
│   └── App.vue
├── statics/               # Icons etc.
├── quasar.config.js       # Quasar config
└── package.json
```

---

## Install Dependencies

```bash
cd templates

yarn install
# or
npm install
```

---

## Configure Backend URL

Edit `src/boot/axios.js` to set the backend API URL:

```js
const baseURL = 'http://127.0.0.1:8000'
const api = axios.create({ baseURL })
```

The backend runs at `http://127.0.0.1:8000` by default.

---

## Development Mode

```bash
# Make sure backend is running
bomiot run

# Start frontend dev server (hot reload)
quasar dev
```

---

## Production Build

```bash
# Output goes to templates/dist/spa/
quasar build
```

> Note: Django serves the `templates/dist/spa/` directory, so you must run `quasar build` after any frontend changes for them to take effect.

---

## Request Wrapper

All API calls go through `src/boot/axios.js`, which exports `get`, `post`, `put`, `patch`, `deleteData`, etc.

Headers are automatically attached:
- `token`: JWT auth token
- `language`: current language (e.g. `en-US`)
- `project`: project identifier (e.g. `bomiot`)

```js
import { get, post } from 'boot/axios'

// GET
const res = await get({ url: 'core/user/', params: { page: 1, max_page: 20 } })

// POST
const res = await post({ url: 'core/user/create/', body: { username: 'admin' } })
```

---

## Pages & Routes

Pages live in `src/pages/`, registered in `src/router/routes.js`:

```js
{ path: 'my-page', component: () => import('pages/MyPage.vue') }
```

---

## Internationalization

Locale files are in `src/i18n/`, supporting `zh-CN` and `en-US`. Use `useI18n` in components:

```js
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
```

---

## Menus & Tabs

- **Tab bar**: `src/components/TabList.vue` defines top tabs
- **Menu**: `src/components/MenuLink.vue` defines sidebar items, grouped by the `tab` field

---

## Documentation Pages

Doc pages render Markdown via the `MDParser` component. Source files live in the backend `greaterwms/media/` directory and are served through the `md/<docName>.<lang>.md` endpoint.
