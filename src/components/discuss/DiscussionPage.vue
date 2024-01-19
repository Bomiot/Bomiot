<template>
  <div class="q-pa-md">
    <Giscus
       id="comments"
       defaultCommentOrder="newest"
       :repo="GiscusStore.repo"
       :repoid="GiscusStore.repoid"
       :category="GiscusStore.category"
       :categoryid="GiscusStore.categoryid"
       mapping="title"
       strict="0"
       reactionsenabled="1"
       emitmetadata="1"
       inputposition="top"
       :theme="darkStore.darkMode ? 'dark_dimmed' : 'light'"
       crossorigin="anonymous"
       :lang=langStore.langData
       loading="lazy"
    />
  </div>
</template>

<script setup>
import { useLanguageStore } from 'stores/language'
import { useDarkStore } from 'stores/dark'
import { useGiscusStore } from "stores/giscus"
import Giscus from '@giscus/vue'
import { useQuasar } from "quasar"
import { onMounted } from "vue"

const $q = useQuasar()
const langStore = useLanguageStore()
const darkStore = useDarkStore()
const GiscusStore = useGiscusStore()

onMounted(() => {

})

</script>
