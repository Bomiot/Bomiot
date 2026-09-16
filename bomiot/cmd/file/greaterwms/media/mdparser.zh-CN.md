# Markdown 渲染（MDParser）

## 文件位置

`src/components/md/MDParser.vue`

## 作用

渲染 Markdown 文档，支持代码高亮、目录生成、数学公式、emoji 等。所有 Reader 页面都使用此组件。

## 数据加载流程

1. `mdDocsStore.docName` 变化（由 DevReader 设置）
2. MDParser watch 到变化，请求后端 `md/<docName>.<lang>.md`
3. 拿到 markdown 文本后用 markdown-it 渲染为 HTML
4. 生成 TOC 目录

```js
watch(() => mdStore.docName, val => {
  if (val) {
    mdDataChange()  // 请求 md/<docName>.<lang>.md
  }
})
```

## 请求文档

```js
function mdDataChange() {
  get({
    url: `md/${mdStore.docNameGet}.${langStore.langGet}.md`,
    params: {}
  }).then(res => {
    mdStore.mdDocsChange(res)
    MDHtml()  // 渲染
  })
}
```

## markdown-it 插件

```js
md.use(markdownItAttrs)          // 属性语法
md.use(markdownItKatex)          // 数学公式
md.use(emoji)                    // emoji
md.use(markdownItCodeCopy, {...}) // 代码复制按钮
md.use(markdownItContainer, 'warning', {...}) // 自定义容器
md.use(markdownItIns)            // 插入文本
md.use(markdownItMark)           // 标记文本
md.use(markdownItDeflist)        // 定义列表
md.use(markdownItAbbr)           // 缩写
md.use(markdownItFootnote)       // 脚注
md.use(markdownItTaskLists, {})  // 任务列表
md.use(markdownItHighlight)      // 代码高亮（monokai 主题）
```

## 代码高亮

使用 `highlight.js` 的 monokai 主题：

```js
highlight: function (str, lang) {
  if (lang && hljs.getLanguage(lang)) {
    return hljs.highlight(str, { language: lang }).value
  }
}
```

## TOC 目录生成

解析渲染后的 HTML，提取所有标题生成目录：

```js
function generateToc(html) {
  const headings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6')
  headings.forEach((heading, index) => {
    const level = parseInt(heading.tagName.charAt(1))
    const id = `heading-${index}`
    heading.id = id
    tocItems.push({ level, text, id })
  })
}
```

## 自动重新渲染

以下情况会自动重新加载文档：
- `docName` 变化（切换文档）
- 语言切换
- 暗黑模式切换
