# 多项目切换

## 概述

GreaterWMS 前端支持在一个界面内切换多个项目（多租户/多项目运行）。切换项目后，所有后续请求会带上新的 `project` 请求头，后端据此返回对应项目的数据。

核心由三部分组成：

1. `stores/project.js` — 存储当前项目名（持久化）
2. `MainLayout.vue` — 项目选择器 UI、加载项目列表、切换后刷新
3. `boot/axios.js` — 读取项目并写入请求头

## 1. project Store

位置：`src/stores/project.js`

```js
import { defineStore } from 'pinia'

export const useProjectStore = defineStore('project', {
  state: () => ({
    project: 'greaterwms'   // 默认项目
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
    enable: true   // 持久化到 LocalStorage
  }
})
```

关键点：

- 默认值为 `greaterwms`
- 通过 `pinia-plugin-persistedstate` 持久化，刷新页面后仍保留
- `projectChange(value)` 是唯一修改入口

## 2. 项目选择器（MainLayout）

MainLayout 头部有一个 `q-select` 项目选择器：

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

### 加载项目列表

页面挂载时调用 `projectlist/` 接口获取可选项目：

```js
async function getProjectList() {
  await get({ url: 'projectlist/', params: {} }).then((res) => {
    projectOptions.value = res.list   // [{ label, value }, ...]
    projectCheck()
  })
}
```

### 回显当前项目

从持久化的 store 中读取当前项目，在选项列表中匹配并回显：

```js
function projectCheck() {
  for (let item of projectOptions.value) {
    if (item.value === projectStore.projectDataGet) {
      projectData.value = item
    }
  }
}
```

### 切换项目

```js
function projectChange (e) {
  let rawData = toRaw(e)
  projectStore.projectChange(rawData.value)
}
```

切换后触发 `watch`，写入 cookie 并重新加载页面：

```js
watch(() => projectStore.project, val => {
  if (val) {
    $q.cookies.set('project', val)
    window.location.reload(true)
  }
})
```

> 切换项目会**整页刷新**，确保所有模块和请求都使用新项目上下文。

## 3. axios 请求头

`boot/axios.js` 请求拦截器读取持久化的项目值并写入请求头：

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

关键点：

- 从 `LocalStorage` 读取（因为 pinia 持久化后存在这里）
- 兜底默认值 `greaterwms`
- 每个请求都带 `project` 请求头

## 4. 后端数据隔离

`project` 请求头不仅用于**读取**时区分项目，后端在**存储**数据时也会把 `project` 作为字段写入数据库，实现数据隔离。

核心机制：

1. **写入时打标**：后端接收到写请求（创建/更新）时，从 `project` 请求头取出项目名，作为数据行的一个字段（如 `project` 列）一并存入。
2. **查询时过滤**：后端处理读请求时，同样从 `project` 请求头取值，在查询条件中加入 `WHERE project = ?`，只返回当前项目的数据。
3. **隔离效果**：不同项目的数据在同一张表中通过 `project` 字段区分，互不干扰。

示意（伪代码）：

```python
# 写入
def create(self, request, *args, **kwargs):
    data = request.data
    data['project'] = request.headers.get('project', 'greaterwms')  # 打标
    serializer = self.serializer_class(data=data)
    serializer.save()

# 查询
def get_queryset(self):
    project = self.request.headers.get('project', 'greaterwms')
    return self.model.objects.filter(project=project)  # 过滤
```

这样前端只需维护一个 `project` 状态，后端保证同表多项目数据互不越权。

## 完整流程图

```
onMounted
  └─ getProjectList()
       └─ GET projectlist/  →  projectOptions
       └─ projectCheck()    →  回显当前项目到 q-select

用户切换项目
  └─ projectChange(e)
       └─ projectStore.projectChange(value)
            └─ watch 触发
                 ├─ $q.cookies.set('project', value)
                 └─ window.location.reload(true)  ← 整页刷新

刷新后
  └─ axios 拦截器读 LocalStorage.project
       └─ config.headers.project = value
```

## 注意事项

1. **切换项目会刷新页面**：所有未保存的表单数据会丢失，业务上应在切换前提示用户。
2. **默认项目**：`greaterwms`，首次访问或清除 LocalStorage 后回到默认项目。
3. **持久化依赖**：项目切换依赖 `pinia-plugin-persistedstate`，不可移除。
4. **后端配合**：后端需根据 `project` 请求头返回对应项目的数据和项目列表。
