<template>
  <q-page class="flex flex-col q-pa-md">
    <div class="row full-width" :style="{ height: `${rowHeight}px` }">
      <div class="col-12 q-pa-md">
        <LineCharts
          v-if="pypiData.series_list.length"
          :title="pypiData.title"
          :x-axis-data="pypiData.xAxis_list"
          :series-data="pypiData.series_list"
          :show-legend="true"
          :chart-height="chartHeight"
          :chart-width="chartWidth"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { get } from 'boot/axios.js'
import { useQuasar } from 'quasar'
import emitter from "boot/bus.js"
import LineCharts from 'components/echarts/LineCharts.vue'

const $q = useQuasar()

const rowHeight = computed(() => $q.screen.height * 0.73 )
const chartWidth = computed(() => $q.screen.width * 0.825)
const chartHeight = rowHeight.value

const pypiData = ref({ title: '', xAxis_list: [],  series_list: [] })

function onRequest () {
  get({
    url: 'core/pypi/charts/',
  }).then(res => {
    pypiData.value = res.pypi_data
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