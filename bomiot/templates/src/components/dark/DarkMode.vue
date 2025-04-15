<template>
  <q-btn dense flat round class="text-yellow" v-show="!darkStore.darkMode" icon="sunny" @click="darkStore.darkModeChange()" >
    <q-tooltip class="bg-indigo" :offset="[15, 15]" content-style="font-size: 12px">
      Dark
    </q-tooltip>
  </q-btn>
  <q-btn dense flat round class="text-yellow" v-show="darkStore.darkMode" icon="nights_stay" @click="darkStore.darkModeChange()" >
    <q-tooltip class="bg-indigo" :offset="[15, 15]" content-style="font-size: 12px">
      Light
    </q-tooltip>
  </q-btn>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDarkStore } from 'stores/dark'
import { LocalStorage, useQuasar } from 'quasar'


const darkStore = useDarkStore()
const $q = useQuasar()


onMounted(() => {
  if ($q.localStorage.has('dark')) {
    $q.dark.set(JSON.parse(LocalStorage.getItem('dark')).darkMode)
  }
})

</script>
