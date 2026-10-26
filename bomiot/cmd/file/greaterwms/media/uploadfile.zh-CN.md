# 文件上传

基于 `q-uploader` 封装的通用文件上传组件，提供多文件队列、进度展示、状态反馈、图片预览与暗黑模式适配。上传中心页面（Upload Center）即由该组件驱动。

- 组件位置：`templates/src/components/upload/UploadFile.vue`
- 使用示例：`templates/src/pages/UploadCenter.vue`

## 组件结构

```text
UploadFile.vue
  ├─ q-uploader（核心：url / headers / multiple / 事件）
  ├─ header 插槽（自定义工具栏）
  └─ list 插槽（自定义文件行）
```

## 核心属性

| 属性 / 事件 | 值 | 说明 |
|---|---|---|
| `:url` | `getUrl` 函数 | 上传地址。返回**相对路径** `core/user/upload/`，与 axios 实例行为一致，同源部署到任何域名/端口都可用 |
| `:headers` | `token` + `language` | 认证令牌与当前语言，随请求头发送，后端据此鉴权并返回对应语言的提示 |
| `multiple` | — | 允许多文件排队上传 |
| `@uploaded` | `onUploaded` | 单文件上传完成回调 |
| `@error` | `onError` | 上传失败回调 |

> **为什么 url 是相对路径**：组件曾经拼接写死的 `http://127.0.0.1:8000`，部署到服务器后会把文件打到访客自己的电脑。改为相对路径后与全站 axios 行为统一——页面由谁服务，请求就打给谁，零配置适配任何部署环境。

## 工具栏（header 插槽）

通过 `scope` 拿到 q-uploader 的运行时状态与方法，自定义了一排操作按钮：

| 按钮 | 显示条件 | 动作 |
|---|---|---|
| 清空队列 | `scope.queuedFiles.length > 0` | `scope.removeQueuedFiles` |
| 移除已上传 | `scope.uploadedFiles.length > 0` | `scope.removeUploadedFiles` |
| 进度指示 | `scope.isUploading` | 显示 spinner |
| 添加文件 | `scope.canAddFiles` | `scope.pickFiles`（配合 `<q-uploader-add-trigger />`） |
| 上传到服务器 | `scope.canUpload` | `scope.upload` |
| 中止上传 | `scope.isUploading` | `scope.abort` |

标题区显示总大小 / 总进度（`scope.uploadSizeLabel` / `scope.uploadProgressLabel`），所有按钮 tooltip 均走 i18n（`upload.*` 词条）。

## 文件行（list 插槽）

每个文件一行，展示：

- **文件名**（超长省略号）
- **状态**：`idle` 显示"挂载"；上传成功显示后端返回的 `msg`（绿底）；失败显示 `detail`（红底）
- **大小 / 进度**：`file.__sizeLabel` / `file.__progressLabel`
- **图片缩略图**：`file.__img` 存在时显示，点击弹出大图预览（`imgShow`，弹窗高度取屏幕 85%）
- **删除按钮**：`scope.removeFile(file)`，暗黑/浅色模式自动切换图标颜色

## 结果回写逻辑

`onUploaded` 负责把后端响应写回文件对象：

```text
response.xhr.responseText 解析为 JSON
  ├─ 含 msg    → file.notice = msg，file.__status = 'uploaded'（绿底展示）
  └─ 含 detail → file.notice = detail（红底展示）
```

因此**后端接口的响应约定**为 JSON：

```json
{ "msg": "Uploaded" }
```

或失败时：

```json
{ "detail": "error reason" }
```

## 与后端接口的约定

| 项 | 约定 |
|---|---|
| 地址 | `POST core/user/upload/`（相对路径，同源） |
| 请求头 | `token`（认证）、`language`（响应语言） |
| 请求体 | multipart/form-data 文件流 |
| 响应 | JSON，成功 `{msg}` / 失败 `{detail}` |

## 复用要点

1. **换接口**：只需改 `getUrl` 返回的路径
2. **换鉴权方式**：调整 `:headers` 数组即可（注意 q-uploader 不走 axios 拦截器，令牌要手动带）
3. **自定义反馈文案**：后端控制 `msg` / `detail` 内容，前端无需改动
4. **需要 axios 能力时**（节流、Loading、统一错误提示）：不要用 q-uploader，改用 `boot/axios` 导出的 `fileUpload(url, formData)`——赞助页上传 build.json 就是这种方式

## 注意事项

- q-uploader 自己发请求，**不经过 axios 实例**：没有 250ms 节流、没有全局 Loading、没有统一 `detail` 弹窗——所以组件内部自己处理 `onUploaded` 状态回写
- 大屏适配：组件高度取屏幕高度 85%、宽度 82.5%；缩略图与删除按钮 `gt-xs` 仅在大屏显示
- 暗黑模式：工具栏底色 `#1D1D1D` / 浅色 `#1972D2`，删除按钮颜色随模式切换
