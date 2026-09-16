# Multi-Project Switching

## Overview

GreaterWMS frontend supports switching between multiple projects (multi-tenant / multi-project runtime) within one UI. After switching, all subsequent requests carry the new `project` header, and the backend returns data for that project.

Three core parts:

1. `stores/project.js` — stores current project name (persisted)
2. `MainLayout.vue` — project selector UI, loads project list, reloads on switch
3. `boot/axios.js` — reads project and injects into request headers

## 1. project Store

Location: `src/stores/project.js`

```js
import { defineStore } from 'pinia'

export const useProjectStore = defineStore('project', {
  state: () => ({
    project: 'greaterwms'   // default project
  }),

  getters: {
    projectDataGet (state) {
      return state.project
    }
  },

  actions: {
    projectChange (e) {
      this.project = e
    }
  },
  persist: {
    enable: true   // persist to LocalStorage
  }
})
```

Key points:

- Default value is `greaterwms`
- Persisted via `pinia-plugin-persistedstate`, survives page reload
- `projectChange(value)` is the only mutation entry point

## 2. Project Selector (MainLayout)

MainLayout header has a `q-select` project selector:

```html
<q-select
  v-model="projectData"
  :options="projectOptions"
  option-label="label"
  option-value="value"
  @update:model-value="projectChange($event)"
>
  ...
</q-select>
```

### Load Project List

On mount, calls `projectlist/` API to get available projects:

```js
async function getProjectList() {
  await get({ url: 'projectlist/', params: {} }).then((res) => {
    projectOptions.value = res.list   // [{ label, value }, ...]
    projectCheck()
  })
}
```

### Echo Current Project

Reads current project from the persisted store, matches it in the options list:

```js
function projectCheck() {
  for (let item of projectOptions.value) {
    if (item.value === projectStore.projectDataGet) {
      projectData.value = item
    }
  }
}
```

### Switch Project

```js
function projectChange (e) {
  let rawData = toRaw(e)
  projectStore.projectChange(rawData.value)
}
```

Switch triggers a `watch` that writes to cookie and reloads the page:

```js
watch(() => projectStore.project, val => {
  if (val) {
    $q.cookies.set('project', val)
    window.location.reload(true)
  }
})
```

> Switching project triggers a **full page reload**, ensuring all modules and requests use the new project context.

## 3. axios Request Header

`boot/axios.js` request interceptor reads the persisted project value and writes it to the header:

```js
let project = 'greaterwms'
if (LocalStorage.has('project')) {
  const projectCheck = JSON.parse(LocalStorage.getItem('project'))
  if (projectCheck !== '') {
    for (const key in projectCheck) {
      if (key === 'project') {
        project = projectCheck[key]
      }
    }
  }
}
config.headers.project = project
```

Key points:

- Reads from `LocalStorage` (because pinia persistence stores it there)
- Falls back to `greaterwms`
- Every request carries the `project` header

## 4. Backend Data Isolation

The `project` header is not only used to **distinguish projects on read** — the backend also stores `project` as a field when **writing** data, achieving data isolation.

Core mechanism:

1. **Tag on write**: when the backend receives a write request (create/update), it extracts the project name from the `project` header and stores it as a field (e.g. the `project` column) on the data row.
2. **Filter on query**: when handling a read request, the backend reads the same header and adds `WHERE project = ?` to the query, returning only the current project's data.
3. **Isolation**: data from different projects lives in the same table but is separated by the `project` field, never interfering.

Illustration (pseudo-code):

```python
# Write
def create(self, request, *args, **kwargs):
    data = request.data
    data['project'] = request.headers.get('project', 'greaterwms')  # tag
    serializer = self.serializer_class(data=data)
    serializer.save()

# Query
def get_queryset(self):
    project = self.request.headers.get('project', 'greaterwms')
    return self.model.objects.filter(project=project)  # filter
```

This way the frontend only maintains a single `project` state, while the backend guarantees cross-project data stays isolated in the same table.

## Full Flow

```
onMounted
  └─ getProjectList()
       └─ GET projectlist/  →  projectOptions
       └─ projectCheck()    →  echo current project into q-select

User switches project
  └─ projectChange(e)
       └─ projectStore.projectChange(value)
            └─ watch fires
                 ├─ $q.cookies.set('project', value)
                 └─ window.location.reload(true)  ← full reload

After reload
  └─ axios interceptor reads LocalStorage.project
       └─ config.headers.project = value
```

## Notes

1. **Switching reloads the page**: unsaved form data will be lost; warn users before switching.
2. **Default project**: `greaterwms`; resets to default after clearing LocalStorage.
3. **Persistence dependency**: relies on `pinia-plugin-persistedstate`; do not remove it.
4. **Backend coordination**: backend must return data and project list based on the `project` header.
