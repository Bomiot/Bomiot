<template>
  <q-page class="flex flex-col q-pa-md">
    <div class="row full-width" :style="{ height: `${rowHeight}px` }">
      <div class="col-12 q-pa-md">
        <TreeMap
          v-if="pidData.series_list.length"
          :title="pidData.title"
          :series-data="pidData.series_list"
          :show-legend="true"
          :chart-height="chartHeight"
          :chart-width="chartWidth"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { get } from 'boot/axios.js'
import { useQuasar } from 'quasar'
import emitter from "boot/bus.js"
import TreeMap from 'components/echarts/TreeMap.vue'

const $q = useQuasar()

const rowHeight = computed(() => $q.screen.height * 0.8 )
const chartWidth = computed(() => $q.screen.width * 0.825)
const chartHeight = rowHeight.value
let intervalId = null

const pidData = ref({ title: '', series_list: [] })

function onRequest () {
  get({
    url: 'core/server/pidcharts/',
  }).then(res => {
    pidData.value = res.pid_data
  }).catch(err => {
    $q.notify({
      type: 'error',
      message: err
    })
    $q.loading.hide()
  })
}

onMounted(() => {
  listenToEvent()
  onRequest()
  intervalId = setInterval(() => {
    onRequest()
  }, 60000)
})

onBeforeUnmount(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
})

function listenToEvent() {
  emitter.on('needLogin', (payload) => {
    if (payload) {
      console.log('needLogin')
    }
  });
}

</script>

<style scoped>
.full-width {
  width: 100%;
}
</style>