<template>
  <q-page class="flex flex-top">
    <TableList />
  </q-page>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, watch, ref } from 'vue'
import { useAppNameStore } from "stores/appName"
import { useLanguageStore } from "stores/language"
import { useMenuDataStore } from "stores/menu"
import { useMeta, useQuasar } from "quasar"
import { useRouter } from 'vue-router'
import TableList from "components/table/TableList.vue"


const $q = useQuasar()
const router = useRouter()
const appNameStore = useAppNameStore()
const langStore = useLanguageStore()
const menuStore = useMenuDataStore()


const darkShow = ref(false)
const title = ref('')
const description = ref('')
const keywords = ref('')

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
})


onBeforeUnmount(() => {
})


watch(() => langStore.langData, val => {
})

watch(() => menuStore.menuData.routerTo, val => {
})

watch(() => $q.dark.isActive, val => {
  darkShow.value = val
})

</script>
