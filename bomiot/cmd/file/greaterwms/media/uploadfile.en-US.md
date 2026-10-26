# File Upload

A reusable upload component built on `q-uploader`, with a multi-file queue, progress display, status feedback, image preview and dark-mode support. The Upload Center page is driven by this component.

- Component: `templates/src/components/upload/UploadFile.vue`
- Usage example: `templates/src/pages/UploadCenter.vue`

## Component Structure

```text
UploadFile.vue
  ├─ q-uploader (core: url / headers / multiple / events)
  ├─ header slot (custom toolbar)
  └─ list slot (custom file rows)
```

## Core Props

| Prop / Event | Value | Description |
|---|---|---|
| `:url` | `getUrl` function | Upload endpoint. Returns the **relative path** `core/user/upload/` — same behavior as the axios instance, works on any domain/port when served same-origin |
| `:headers` | `token` + `language` | Auth token and current language, sent as request headers so the backend can authenticate and reply in the right language |
| `multiple` | — | Allows queueing multiple files |
| `@uploaded` | `onUploaded` | Per-file upload completion callback |
| `@error` | `onError` | Upload failure callback |

> **Why a relative url**: the component used to concatenate a hardcoded `http://127.0.0.1:8000`, which on a deployed server would post files to the visitor's own machine. The relative path matches the axios behavior used across the app — requests go to whoever serves the page, with zero per-environment configuration.

## Toolbar (header slot)

The `scope` object exposes q-uploader's runtime state and methods, driving a row of custom buttons:

| Button | Visible when | Action |
|---|---|---|
| Clear queue | `scope.queuedFiles.length > 0` | `scope.removeQueuedFiles` |
| Remove uploaded | `scope.uploadedFiles.length > 0` | `scope.removeUploadedFiles` |
| Progress | `scope.isUploading` | Shows a spinner |
| Add files | `scope.canAddFiles` | `scope.pickFiles` (with `<q-uploader-add-trigger />`) |
| Upload to server | `scope.canUpload` | `scope.upload` |
| Abort | `scope.isUploading` | `scope.abort` |

The title area shows total size / total progress (`scope.uploadSizeLabel` / `scope.uploadProgressLabel`); every button tooltip is localized (`upload.*` entries).

## File Rows (list slot)

Each file renders as a row showing:

- **File name** (ellipsis on overflow)
- **Status**: `idle` shows "Idle"; success shows the backend `msg` on green; failure shows `detail` on red
- **Size / progress**: `file.__sizeLabel` / `file.__progressLabel`
- **Image thumbnail**: shown when `file.__img` exists; clicking opens a large preview dialog (`imgShow`, height 85% of screen)
- **Delete button**: `scope.removeFile(file)`; icon color follows dark/light mode

## Result Write-back

`onUploaded` writes the backend response back onto the file object:

```text
Parse response.xhr.responseText as JSON
  ├─ has msg    → file.notice = msg, file.__status = 'uploaded' (green)
  └─ has detail → file.notice = detail (red)
```

So the **backend response contract** is JSON:

```json
{ "msg": "Uploaded" }
```

or on failure:

```json
{ "detail": "error reason" }
```

## Backend Contract

| Item | Contract |
|---|---|
| Endpoint | `POST core/user/upload/` (relative, same-origin) |
| Headers | `token` (auth), `language` (response language) |
| Body | multipart/form-data file stream |
| Response | JSON — success `{msg}` / failure `{detail}` |

## Reuse Notes

1. **Different endpoint**: just change the path returned by `getUrl`
2. **Different auth**: adjust the `:headers` array (q-uploader bypasses the axios interceptors, so the token must be attached manually)
3. **Custom feedback text**: controlled by the backend via `msg` / `detail` — no frontend change needed
4. **When you need axios features** (throttling, Loading, unified error notifications): skip q-uploader and use `fileUpload(url, formData)` from `boot/axios` — that is how the sponsor page uploads build.json

## Notes

- q-uploader issues its own requests and **does not go through the axios instance**: no 250ms throttle, no global Loading, no unified `detail` notification — which is why the component writes back statuses itself in `onUploaded`
- Sizing: height 85% and width 82.5% of the screen; thumbnails and delete buttons are `gt-xs` (large screens only)
- Dark mode: toolbar background `#1D1D1D` vs `#1972D2` in light mode; the delete button color switches accordingly
