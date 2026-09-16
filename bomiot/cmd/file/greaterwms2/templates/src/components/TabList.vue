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
  { name: 'guide', label: t('menuTab.guide') },
  { name: 'deploy', label: t('menuTab.deploy') },
  { name: 'download', label: t('menuTab.download') },
  { name: 'operation', label: t('menuTab.operation') },
  { name: 'product', label: t('menuTab.product') },
  { name: 'contact', label: t('menuTab.contact') },
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
