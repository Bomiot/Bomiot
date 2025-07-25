<template>
  <q-tabs mobile-arrows v-model="tab" align="left" :indicator-color="$q.dark.isActive ? 'yellow' : 'black'">
    <q-tab v-for="(list, index) in tabList"
           :key="index"
           v-bind="list"
           :name="list.name"
           :label="list.label"
           @click="tabChange(list.name)" />
  </q-tabs>
</template>

<script setup>
import { computed, watch, ref, onMounted } from 'vue'
import { useI18n } from "vue-i18n"
import { useTabDataStore } from 'stores/tab'
import { useQuasar } from "quasar"

const $q = useQuasar()
const { t } = useI18n()
const tabStore = useTabDataStore()

const tab = ref('')

const tabList = computed(() => [
  { name: 'standard', label: t('menuTab.standard') },
  { name: 'server', label: t('menuTab.server') },
  { name: 'basic', label: t('menuTab.basic') },
  { name: 'db', label: t('menuTab.db') },
  { name: 'signals', label: t('menuTab.signals') },
  // { name: 'component', label: t('menuTab.component') },
])

function tabChange (e) {
  tabStore.tabDataChange(e)
}

onMounted(() => {
  tab.value = tabStore.tabData
})

watch(() => tabStore.tabData, val => {
  tab.value = val
})

</script>
