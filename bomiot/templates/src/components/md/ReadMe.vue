<template>
  <q-page class="flex flex-top">
    <div id="markdownData" class='markdownStyle' v-html="markdownDom" style="margin-top: 25px; width: 95%; max-width: 95%"></div>
  </q-page>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, watch, ref } from 'vue'
import { useMDDataStore } from "stores/mdDocs"
import { useAppNameStore } from "stores/appName"
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
import markdownItMergeCells from 'markdown-it-merge-cells'
import markdownItCodeCopy from 'markdown-it-code-copy'
import 'highlight.js/styles/monokai.css'
import { useMeta, useQuasar } from "quasar"
import { useLanguageStore } from 'stores/language'
import * as echarts from 'echarts'


const $q = useQuasar()
const mdStore = useMDDataStore()
const langStore = useLanguageStore()
const appNameStore = useAppNameStore()
const rightDrawerStore = userightDrawerStore()

const source = computed(() => mdStore.mdDocs)
const markdownDom = ref('')
const darkShow = ref(false)
const title = ref('')
const description = ref('')
const keywords = ref('')
const echartsInstances = new Map()

function MDHtml() {
  if ($q.dark.isActive) {
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      brakes: true,
      typography: true,
  })
    md.use(markdownItAttrs)
    md.use(markdownItKatex)
    md.use(emoji)
    md.use(markdownItMergeCells)
    md.use(markdownItCodeCopy, {
      containerClass: 'markdown-copy-code-container',
      buttonClass: 'markdown-copy-code-button',
      copySVGClass: 'markdown-copy-code-copy',
      doneSVGClass: 'markdown-copy-code-done'
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
    source.value.split('\r').some((item => {
      if (item.length > 4) {
        item.split('#').some((res => {
          if (res.length > 4) {
            title.value = `${appNameStore.appName} | ${res}`
            description.value = `${appNameStore.appName} | ${res}`
            keywords.value = `${appNameStore.appName} | ${res}`
          }
        }))
        return true
      }
    }))
    markdownDom.value = html
  } else {
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      brakes: true,
      typography: true,
    })
    md.use(markdownItAttrs)
    md.use(markdownItKatex)
    md.use(emoji)
    md.use(markdownItMergeCells)
    md.use(markdownItCodeCopy, {
      containerClass: 'markdown-copy-code-container',
      buttonClass: 'markdown-copy-code-button',
      copySVGClass: 'markdown-copy-code-copy',
      doneSVGClass: 'markdown-copy-code-done'
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
    source.value.split('\r').some((item => {
      if (item.length > 4) {
        item.split('#').some((res => {
          if (res.length > 4) {
            title.value = `${appNameStore.appName} | ${res}`
            description.value = `${appNameStore.appName} | ${res}`
            keywords.value = `${appNameStore.appName} | ${res}`
          }
        }))
        return true
      }
    }))
    markdownDom.value = html
  }
}

function mdDataChange() {
  get({
    url: `md/README.${langStore.langData}.md`,
    params: {}
  }).then(res => {
    if (!res.detail) {
      get({
        url: res,
        params: {}
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
  echartsInstances.forEach(chart => echarts.dispose(chart));
  echartsInstances.clear();
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

</script>
