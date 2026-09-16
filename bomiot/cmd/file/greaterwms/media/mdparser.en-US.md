# Markdown Parser (MDParser)

## Location

`src/components/md/MDParser.vue`

## Purpose

Renders Markdown docs with syntax highlighting, TOC, math, emoji. Used by all Reader pages.

## Data Flow

1. `mdDocsStore.docName` changes (set by DevReader)
2. MDParser watches, requests `md/<docName>.<lang>.md`
3. Renders markdown to HTML via markdown-it
4. Generates TOC

```js
watch(() => mdStore.docName, val => {
  if (val) mdDataChange()
})
```

## Request Doc

```js
function mdDataChange() {
  get({
    url: `md/${mdStore.docNameGet}.${langStore.langGet}.md`,
    params: {}
  }).then(res => {
    mdStore.mdDocsChange(res)
    MDHtml()
  })
}
```

## markdown-it Plugins

```js
md.use(markdownItAttrs)          // attribute syntax
md.use(markdownItKatex)          // math
md.use(emoji)                    // emoji
md.use(markdownItCodeCopy, {...}) // copy button
md.use(markdownItContainer, 'warning', {...}) // custom container
md.use(markdownItIns)            // inserted text
md.use(markdownItMark)           // marked text
md.use(markdownItDeflist)        // definition list
md.use(markdownItAbbr)           // abbreviation
md.use(markdownItFootnote)       // footnote
md.use(markdownItTaskLists, {})  // task list
md.use(markdownItHighlight)      // code highlight (monokai)
```

## Code Highlighting

Uses `highlight.js` monokai theme:

```js
highlight: function (str, lang) {
  if (lang && hljs.getLanguage(lang)) {
    return hljs.highlight(str, { language: lang }).value
  }
}
```

## TOC Generation

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

## Auto Reload Triggers

- `docName` change
- Language switch
- Dark mode switch
