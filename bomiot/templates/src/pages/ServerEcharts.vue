<template>
  <q-page class="flex flex-col q-pa-md">
    <div class="row full-width" :style="{ height: `${rowHeight}px` }">
      <div class="col-6 q-pa-md">
        <LineCharts
          v-if="cpuData.series_list.length"
          :title="cpuData.title"
          :x-axis-data="cpuData.xAxis_list"
          :series-data="cpuData.series_list"
          :show-legend="true"
          :chart-height="chartHeight"
          :chart-width="chartWidth"
        />
      </div>
      <div class="col-6 q-pa-md">
        <StackedBar
          v-if="memoryData.series_list.length"
          :title="memoryData.title"
          :x-axis-data="memoryData.xAxis_list"
          :series-data="memoryData.series_list"
          :show-legend="true"
          :chart-height="chartHeight"
          :chart-width="chartWidth"
        />
      </div>
    </div>

    <div class="row full-width" :style="{ height: `${rowHeight}px` }">
      <div class="col-6 q-pa-md">
        <StackedBar
          v-if="diskData.series_list.length"
          :title="diskData.title"
          :x-axis-data="diskData.xAxis_list"
          :series-data="diskData.series_list"
          :show-legend="true"
          :chart-height="chartHeight"
          :chart-width="chartWidth"
        />
      </div>
      <div class="col-6 q-pa-md">
        <StackedLine
          v-if="networkData.series_list.length"
          :title="networkData.title"
          :x-axis-data="networkData.xAxis_list"
          :series-data="networkData.series_list"
          :show-legend="true"
          :chart-height="chartHeight"
          :chart-width="chartWidth"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { get } from 'boot/axios'
import { useLanguageStore } from 'stores/language'
import { useQuasar } from 'quasar'
import emitter from "boot/bus.js"
import StackedLine from 'components/echarts/StackedLine.vue'
import LineCharts from 'components/echarts/LineCharts.vue'
import StackedBar from 'components/echarts/StackedBar.vue'

const $q = useQuasar()
const langStore = useLanguageStore()

const rowHeight = computed(() => $q.screen.height * 0.73 / 2 )
const chartWidth = computed(() => $q.screen.width * 0.825)
const chartHeight = rowHeight.value
let intervalId = null

const cpuData = ref({ title: '', xAxis_list: [], series_list: [] })
const memoryData = ref({ title: '', xAxis_list: [], series_list: [] })
const diskData = ref({ title: '', xAxis_list: [], series_list: [] })
const networkData = ref({ title: '', xAxis_list: [], series_list: [] })

function onRequest () {
  get({
    url: 'core/server/echarts/',
  }).then(res => {
    cpuData.value = res.cpu_data
    memoryData.value = res.memory_data
    diskData.value = res.disk_data
    networkData.value = res.network_data
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

watch(() => langStore.langData, val => {
  if (val) {
    onRequest()
  }
})

</script>

<style scoped>
.full-width {
  width: 98%;
}
</style>