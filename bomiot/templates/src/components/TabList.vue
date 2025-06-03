<template>
  <q-tabs mobile-arrows v-model="tab" align="left" :indicator-color="indicatorColor">
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
const indicatorColor = ref('black')

const tabList = computed(() => [
  { name: 'standard', label: t('menuTab.standard') },
  { name: 'server', label: t('menuTab.server') },
  { name: 'api', label: 'api' },
])

function tabColor () {
  if ($q.dark.isActive) {
    indicatorColor.value = 'yellow'
  } else {
    indicatorColor.value = 'black'
  }
}

function tabChange (e) {
  tabStore.tabDataChange(e)
}

onMounted(() => {
  tab.value = tabStore.tabData
  tabColor()
})

watch(() => tabStore.tabData, val => {
  tab.value = val
})

watch(() => $q.dark.isActive, val => {
  if (val) {
    tabColor()
  }
})

</script>
