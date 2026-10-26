<template>
  <q-btn
    round
    dense
    flat
    color="white"
    icon="translate"
    style="margin: 0 10px 0 10px"
  >
    <q-menu>
      <q-list style="min-width: 100px">
        <q-item
          clickable
          v-close-popup
          v-for="(language, index) in langOptions"
          :key="index"
          @click="ChangeLanguage(language.value)"
        >
          <q-item-section>{{ language.label }}</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script setup>
import { computed, watch, onMounted } from 'vue'
import { useLanguageStore } from 'stores/language'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'

const langStore = useLanguageStore()
const $q = useQuasar()

const lang = computed(() => langStore.langData)
const { locale } = useI18n({ useScope: 'global' })
const langOptions = computed(() => langStore.langOptionsData)

function ChangeLanguage(e) {
  langStore.LangChange(e)
}

onMounted(() => {
  if ($q.localStorage.has('language')) {
    locale.value = JSON.parse($q.localStorage.getItem('language')).langData
  } else {
    if ($q.lang.getLocale() === 'zh-CN') {
      locale.value = 'zh-CN'
      ChangeLanguage(locale.value)
    } else {
      locale.value = 'en-US'
      ChangeLanguage(locale.value)
    }
  }
})

watch(lang, (newValue, oldValue) => {
  locale.value = oldValue
  locale.value = newValue
})

</script>
