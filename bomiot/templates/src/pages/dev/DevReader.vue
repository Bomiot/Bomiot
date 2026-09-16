<template>
  <q-page class="flex flex-top">
    <MDParser />
  </q-page>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useMeta } from "quasar"
import { useRoute } from 'vue-router'
import { useMDDataStore } from 'stores/mdDocs'
import MDParser from "components/md/MDParser.vue"

const title = ref('')
const description = ref('')
const keywords = ref('')

const route = useRoute()
const mdDataStore = useMDDataStore()

useMeta(() => {
  return {
    title: title.value,
    meta: {
        description: { name: 'description', content: description.value },
        keywords: { name: 'keywords', content: keywords.value },
      }
    }
  })

function updateDocName () {
  // Derive docName from route path: /dev-quickstart -> quickstart
  const name = route.path.replace(/^\/dev-/, '')
  if (name) {
    mdDataStore.docNameChange(name)
  }
}

onMounted (() => {
  updateDocName()
})

// Vue Router 复用同一组件时 onMounted 不会重跑，必须 watch route 变化
watch(() => route.path, () => {
  updateDocName()
})


onBeforeUnmount(() => {
})

</script>
