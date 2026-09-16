<template>
  <div class="q-pa-md">
    <q-table
      :class="$q.dark.isActive?'my-sticky-header-column-table-dark' : 'my-sticky-header-column-table'"
      flat
      bordered
      :rows="rows"
      :columns="columns"
      row-key="index"
      v-model:pagination="pagination"
      separator="cell"
      :no-data-label="t('nodata')"
      :rows-per-page-label="t('per_page')"
      :rows-per-page-options="[10,30,50,200,1000]"
      :table-style="{ height: ScreenHeight, width: ScreenWidth }"
      :card-style="{ backgroundColor: CardBackground }"
      @request="onRequest"

    >
      <template v-slot:top="props">
        <q-btn-group flat>
          <q-btn :label="t('refresh')" icon="refresh" @click="onRequest()">
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('refreshdata') }}</q-tooltip>
          </q-btn>
        </q-btn-group>
        <q-space />
        <q-btn
          flat round dense
          :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
          @click="props.toggleFullscreen"
        />
      </template>

      <template v-slot:body-cell="props">
        <q-td :props="props">
          {{ props.value }}
        </q-td>
      </template>

      <template v-slot:pagination>
        {{ t('total') }}{{ pagesNumber }} {{ t('page') }}
        <q-pagination
          v-model="pagination.page"
          :max="pagesNumber"
          input
          input-class="text-orange-10"
          @update:model-value="onRequest()"
        />
      </template>

    </q-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useI18n } from "vue-i18n"
import { get } from 'boot/axios'
import { useTokenStore } from 'stores/token'
import { useLanguageStore } from 'stores/language'
import emitter from "boot/bus.js";

const { t } = useI18n()
const $q = useQuasar()
const tokenStore = useTokenStore()
const langStore = useLanguageStore()

const columns = computed( () => [
  { name: 'cpu_frequency', required: true, label: t('cpu.cpu_frequency'), align: 'left', field: 'cpu_frequency'},
  { name: 'min_cpu_frequency', align: 'center', label: t('cpu.min_cpu_frequency'), field: 'min_cpu_frequency' },
  { name: 'max_cpu_frequency', align: 'center' ,label: t('cpu.max_cpu_frequency'), field: 'max_cpu_frequency' },
  { name: 'physical_cores', align: 'center', label: t('cpu.physical_cores'), field: 'physical_cores' },
  { name: 'logical_cores', align: 'center', label: t('cpu.logical_cores'), field: 'logical_cores' },
  { name: 'cpu_usage', align: 'center', label: t('cpu.cpu_usage'), field: 'cpu_usage' },
  { name: 'updated_time', align: 'center', label: t('updated_time'), field: 'updated_time' },

])

const token = computed(() => tokenStore.token)
const rows = ref( [])
const userList = ref( [])
const rowsCount = ref(0)
let intervalId = null

const pagination  = ref({
    sortBy: 'updated_time',
    descending: false,
    page: 1,
    rowsPerPage: 30,
    rowsNumber: 30
  })

const pagesNumber = computed( () => {
  if (token.value !== '') {
    return Math.ceil(rowsCount.value / pagination.value.rowsPerPage)
  } else {
    return 0
  }
})

const ScreenHeight = ref($q.screen.height * 0.73 + '' + 'px')
const ScreenWidth = ref($q.screen.width * 0.825 + '' + 'px')
const CardBackground = ref($q.dark.isActive? '#121212' : '#ffffff')

function onRequest (props) {
  let requestData = {}
  if (props) {
    requestData = props
  } else {
    requestData.pagination = pagination.value
  }
  if (tokenStore.tokenDataGet !== '') {
    get({
      url: 'core/cpu/',
      params: {
        page: requestData.pagination.page,
        max_page: requestData.pagination.rowsPerPage
      }
    }).then(res => {
      rows.value = res.results.map(item => {
        return {
          ...item,
          cpu_frequency: item.cpu_frequency,
          min_cpu_frequency: item.min_cpu_frequency,
          max_cpu_frequency: item.max_cpu_frequency,
          physical_cores: item.physical_cores,
          logical_cores: item.logical_cores,
          cpu_usage: item.cpu_usage + '%',
          updated_time: item.updated_time
        }
      })
      rowsCount.value = res.count
      userList.value = res.users
    }).catch(err => {
      $q.notify({
        type: 'error',
        message: err
      })
      $q.loading.hide()
    })
    pagination.value = requestData.pagination
  }
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

watch(() => $q.dark.isActive, val => {
  CardBackground.value = val? '#121212' : '#ffffff'
})

function listenToEvent() {
  emitter.on('needLogin', (payload) => {
    if (payload) {
      rows.value = []
      userList.value = []
      rowsCount.value = 0
    }
  });
}

watch(() => langStore.langData, val => {
  if (val) {
    onRequest()
  }
})

</script>
