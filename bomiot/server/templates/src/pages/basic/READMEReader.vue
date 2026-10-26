<template>
  <q-page class="flex flex-top">
    <MDParser />
  </q-page>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useMeta } from "quasar"
import { useMDDataStore } from 'stores/mdDocs'
import MDParser from "components/md/MDParser.vue"

const title = ref('')
const description = ref('')
const keywords = ref('')

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


onMounted (() => {
  mdDataStore.docNameChange('README')
})


onBeforeUnmount(() => {
})

</script>
