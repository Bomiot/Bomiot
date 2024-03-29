<template>
  <q-page class="flex flex-top">
    <div id="markdownData" v-html="markdownDom" style="margin-top: 25px; width: 95%; max-width: 95%"></div>
    <DiscussionPage style="margin-bottom: 200px; width: 95%"/>
  </q-page>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, watch, ref } from 'vue'
import { useMDDataStore } from "stores/mdDocs"
import { useAppNameStore } from "stores/appName"
import { useLanguageStore } from "stores/language"
import { useMenuDataStore } from "stores/menu"
import { userightDrawerStore } from "stores/rightDrawer"
import DiscussionPage from "components/discuss/DiscussionPage.vue"
import MarkdownIt from 'markdown-it'
import { full as emoji } from 'markdown-it-emoji'
import markdownItKatex from 'markdown-it-katex'
import markdownItContainer from 'markdown-it-container'
import markdownItAnchor from 'markdown-it-anchor'
import markdownItTocDoneRight from 'markdown-it-toc-done-right'
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
import { useRouter } from 'vue-router'


const $q = useQuasar()
const router = useRouter()
const mdStore = useMDDataStore()
const appNameStore = useAppNameStore()
const langStore = useLanguageStore()
const menuStore = useMenuDataStore()
const rightDrawerStore = userightDrawerStore()


const source = computed(() => mdStore.mdDocs)
const markdownDom = ref('')
const darkShow = ref(false)
const title = ref('')
const description = ref('')
const keywords = ref('')


function MDHtml () {
  if ($q.dark.isActive) {
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      brakes: true,
      typography: true
    })
    md.use(markdownItAttrs)
    md.use(markdownItKatex)
    md.use(emoji)
    md.use(markdownItMergeCells)
    md.use(markdownItCodeCopy)
    md.use(markdownItContainer, 'warning', {
      validate: function(params) {
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
    md.use(markdownItAnchor, { permalink: true, permalinkBefore: true, permalinkSymbol: '' })
    md.use(markdownItTocDoneRight, {
        containerId: 'toc',
        listType: 'ul',
        listClass: 'listClass',
        linkClass: 'linkDarkClass',
        callback: function (html, ) {
        if (html.length < 50) {
          router.push('/404')
        } else {
          mdStore.tocRouterChange(html)
        }
      }
    })
    md.use(markdownItFootnote)
    md.use(markdownItTaskLists, {})
    md.use(markdownItHighlight)
    const html = md.render(source.value)
    markdownDom.value = html
    source.value.split('\r').some((item => {
      if (item.length > 4) {
        item.split('#').some((res => {
          if (res.length > 4) {
            title.value = `${appNameStore.appName} |${res}`
            description.value = `${appNameStore.appName} |${res}`
            keywords.value = `${appNameStore.appName} |${res}`
          }
        }))
        return true
      }
    }))
  } else {
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      typography: true
    })
    md.use(markdownItAttrs)
    md.use(markdownItKatex)
    md.use(emoji)
    md.use(markdownItMergeCells)
    md.use(markdownItCodeCopy)
    md.use(markdownItContainer, 'warning', {
      validate: function(params) {
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
    md.use(markdownItAnchor, { permalink: true, permalinkBefore: true, permalinkSymbol: '' })
    md.use(markdownItTocDoneRight, {
        containerId: 'toc',
        listType: 'ul',
        listClass: 'listClass',
        linkClass: 'linkClass',
        callback: function (html, ) {
        if (html.length < 50) {
          router.push('/404')
        } else {
          mdStore.tocRouterChange(html)
        }
      }
    })
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

function getMD (name) {
  const xhr = new XMLHttpRequest()
  const okStatus = document.location.protocol === 'file:' ? 0 : 200
  xhr.open('GET', '../../md/' + name + '.md', false)
  xhr.overrideMimeType('text/html; charset=utf-8')
  xhr.send(null)
  return xhr.status === okStatus ? xhr.responseText : null
}


function mdDataChange () {
  let data = getMD(menuStore.menuData.link.split('/')[2] + '.' + langStore.langData)
  if (data === null) {
    router.push('/404')
  } else {
    mdStore.mdDocsChange(data)
    MDHtml()
  }

}

useMeta(() => {
  return {
    title: title.value,
    meta: {
        description: { name: 'description', content: description.value },
        keywords: { name: 'keywords', content: keywords.value },
      }
    }
  })


onMounted (() => {
  mdDataChange()
  rightDrawerStore.controlRightDrawer(true)
})


onBeforeUnmount(() => {
  rightDrawerStore.controlRightDrawer(false)
})


watch(() => langStore.langData, val => {
  mdDataChange()
})

watch(() => menuStore.menuData.routerTo, val => {
  if (val !== '/') {
    mdDataChange()
  }
})

watch(() => $q.dark.isActive, val => {
  darkShow.value = val
  mdDataChange()
})

</script>
