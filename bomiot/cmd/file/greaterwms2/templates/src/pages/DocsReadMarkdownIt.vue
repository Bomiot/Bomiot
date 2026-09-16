<template>
  <q-page class="flex flex-top">
    <MDParser />
  </q-page>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { useMeta } from 'quasar'
import { useMDDataStore } from 'stores/mdDocs'
import { useLanguageStore } from 'stores/language'
import MDParser from 'components/md/MDParser.vue'

const route = useRoute()
const mdDataStore = useMDDataStore()
const langStore = useLanguageStore()

const title = ref('')
const description = ref('')
const keywords = ref('')

useMeta(() => {
  return {
    title: title.value,
    meta: {
      description: { name: 'description', content: description.value },
      keywords: { name: 'keywords', content: keywords.value }
    }
  }
})

function loadDoc() {
  const mdDocs = route.params.md_docs
  if (mdDocs) {
    const lang = route.params.lang || langStore.langGet
    if (lang && lang !== langStore.langGet) {
      langStore.LangChange(lang)
    }
    mdDataStore.docNameChange(mdDocs)
    title.value = `${mdDocs} | GreaterWMS`
    description.value = `${mdDocs} | GreaterWMS`
    keywords.value = `${mdDocs} | GreaterWMS`
  }
}

onMounted(() => {
  loadDoc()
})

onBeforeUnmount(() => {
  mdDataStore.docNameChange('')
})

watch(() => route.params.md_docs, () => {
  loadDoc()
})

watch(() => route.params.lang, () => {
  loadDoc()
})
</script>
