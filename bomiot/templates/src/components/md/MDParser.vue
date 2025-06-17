<template>
  <div id="markdownData" :class="[$q.dark.isActive ? 'markdownStyle-dark' : 'markdownStyle', { 'fade-in': markdownDom }]" v-html="markdownDom" style="margin-top: 25px; width: 80%; max-width: 80%"></div>
  <div :class="[$q.dark.isActive ? 'toc-container-dark' : 'toc-container']" v-if="toc.length > 0">
    <div class="toc-title">{{ t('contents') }}</div>
    <div class="toc-content">
      <div v-for="(item, index) in toc"
            :key="index"
            :class="['toc-item', `toc-level-${item.level}`]">
        {{ item.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, watch, ref } from 'vue'
import { useMDDataStore } from "stores/mdDocs"
import { userightDrawerStore } from "stores/rightDrawer"
import { get } from 'boot/axios'
import MarkdownIt from 'markdown-it'
import { full as emoji } from 'markdown-it-emoji'
import markdownItKatex from 'markdown-it-katex'
import markdownItContainer from 'markdown-it-container'
import markdownItAttrs from 'markdown-it-attrs'
import markdownItFootnote from 'markdown-it-footnote'
import markdownItTaskLists from 'markdown-it-task-lists'
import markdownItHighlight from 'markdown-it-highlightjs'
import markdownItIns from 'markdown-it-ins'
import markdownItMark from 'markdown-it-mark'
import markdownItDeflist from 'markdown-it-deflist'
import markdownItAbbr from 'markdown-it-abbr'
import markdownItCodeCopy from 'markdown-it-code-copy'
import 'highlight.js/styles/monokai.css'
import { useMeta, useQuasar } from "quasar"
import { useLanguageStore } from 'stores/language'
import hljs from 'highlight.js'
import { useI18n } from "vue-i18n"

const { t } = useI18n()
const $q = useQuasar()
const mdStore = useMDDataStore()
const langStore = useLanguageStore()
const rightDrawerStore = userightDrawerStore()

const source = computed(() => mdStore.mdDocsGet)
const markdownDom = ref('')
const darkShow = ref(false)
const title = ref('')
const description = ref('')
const keywords = ref('')
const toc = ref([])
const copyText = ref('')

function generateToc(html) {
  const parser = new DOMParser()
  const doc = parser.parseFromString(html, 'text/html')
  const headings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6')
  const tocItems = []

  headings.forEach((heading, index) => {
    const level = parseInt(heading.tagName.charAt(1))
    const text = heading.textContent
    const id = `heading-${index}`
    heading.id = id
    heading.style.scrollMarginTop = '80px'
    tocItems.push({ level, text, id })
  })

  toc.value = tocItems
}

function MDHtml() {
  if ($q.dark.isActive) {
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      brakes: true,
      typography: true,
      highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(str, { language: lang }).value;
          } catch (error) {
            console.warn('Highlight error:', error);
          }
        }
        return '';
      }
    })
    md.use(markdownItAttrs)
    md.use(markdownItKatex)
    md.use(emoji)
    md.use(markdownItCodeCopy, {
      iconStyle: 'font-size: 21px; opacity: 0.4; color: #fff',
      iconClass: 'mdi mdi-content-copy',
      buttonStyle: 'position: absolute; top: 7.5px; right: 6px; cursor: pointer; outline: none; background-color: transparent;',
      buttonClass: '',
      onSuccess: function(e) {
        copyText.value = e.text
      }
    })
    md.use(markdownItContainer, 'warning', {
      validate: function (params) {
        return params
      },
      render: function (tokens, idx) {
        var m = tokens[idx].info
        if (tokens[idx].nesting === 1) {
          return '<details style="background: yellowgreen; color: black; "><summary>' + md.utils.escapeHtml(m) + '</summary>\n'
        } else {
          return '</details>\n'
        }
      },
    })
    md.use(markdownItIns)
    md.use(markdownItMark)
    md.use(markdownItDeflist)
    md.use(markdownItAbbr)
    md.use(markdownItFootnote)
    md.use(markdownItTaskLists, {})
    md.use(markdownItHighlight)
    const html = md.render(source.value)
    generateToc(html)
    markdownDom.value = ''
    setTimeout(() => {
      markdownDom.value = html
    }, 225)
  } else {
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      brakes: true,
      typography: true,
      highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(str, { language: lang }).value;
          } catch (error) {
            console.warn('Highlight error:', error);
          }
        }
        return '';
      }
    })
    md.use(markdownItAttrs)
    md.use(markdownItKatex)
    md.use(emoji)
    md.use(markdownItCodeCopy, {
      iconStyle: 'font-size: 21px; opacity: 0.4; color: #fff;',
      iconClass: 'mdi mdi-content-copy',
      buttonStyle: 'position: absolute; top: 7.5px; right: 6px; cursor: pointer; outline: none; background-color: transparent;',
      buttonClass: '',
      onSuccess: function(e) {
        copyText.value = e.text
      }
    })
    md.use(markdownItContainer, 'warning', {
      validate: function (params) {
        return params
      },
      render: function (tokens, idx) {
        var m = tokens[idx].info
        if (tokens[idx].nesting === 1) {
          return '<details style="background: yellowgreen; color: black; "><summary>' + md.utils.escapeHtml(m) + '</summary>\n'
        } else {
          return '</details>\n'
        }
      },
    })
    md.use(markdownItIns)
    md.use(markdownItMark)
    md.use(markdownItDeflist)
    md.use(markdownItAbbr)
    md.use(markdownItFootnote)
    md.use(markdownItTaskLists, {})
    md.use(markdownItHighlight)
    const html = md.render(source.value)
    generateToc(html)
    markdownDom.value = ''
    setTimeout(() => {
      markdownDom.value = html
    }, 225)
  }
}

function mdDataChange() {
  get({
    url: `md/${mdStore.docNameGet}.${langStore.langGet}.md`,
    params: {},
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    },
    timestamp: new Date().getTime()
  }).then(res => {
    if (!res.detail) {
      get({
        url: res,
        params: {},
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        },
        timestamp: new Date().getTime()
      }).then(res => {
        mdStore.mdDocsChange(res)
        MDHtml()
      }).catch(err => {
        $q.loading.hide()
        return Promise.reject(err)
      })
    } else {
      $q.loading.hide()
      return Promise.reject(new Error('Failed to load README file'))
    }
  }).catch(err => {
    $q.loading.hide()
    return Promise.reject(err)
  })
}


useMeta(() => {
  return {
    title: title.value,
    meta: {
      description: {name: 'description', content: description.value},
      keywords: {name: 'keywords', content: keywords.value},
    }
  }
})


onMounted(() => {
  mdDataChange()
})


onBeforeUnmount(() => {
  rightDrawerStore.controlRightDrawer(false)
  rightDrawerStore.controlRightDrawer(false)
})


watch(() => $q.dark.isActive, val => {
  darkShow.value = val
  mdDataChange()
})

watch(() => langStore.langData, val => {
  if (val) {
    mdDataChange()
  }
})

watch(() => copyText.value, val => {
  if (val) {
    $q.notify({
      type: 'success',
      message: t('copySuccess'),
    })
  }
})

watch(() => mdStore.docName, val => {
  if (val) {
    mdDataChange()
  }
})

</script>
