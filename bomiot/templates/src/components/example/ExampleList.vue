
<template>
  <div class="q-pa-md">
    <q-table
      :class="$q.dark.isActive ? 'my-sticky-header-last-column-table-dark' : 'my-sticky-header-last-column-table'"
      flat
      bordered
      :rows="rows"
      :columns="columns"
      row-key="index"
      v-model:pagination="pagination"
      separator="cell"
      :no-data-label="t('nodata')"
      :rows-per-page-label="t('per_page')"
      :rows-per-page-options="[30, 50, 200, 1000]"
      :table-style="{ height: screenHeight, width: screenWidth }"
      :card-style="{ backgroundColor: cardBackground }"
      @request="onRequest"
    >
      <template v-slot:top="props">
        <q-btn-group flat>
          <q-btn
            :label="t('refresh')"
            icon="refresh"
            @click="onRequest()"
          >
            <q-tooltip
              class="bg-indigo"
              :offset="[10, 10]"
              content-style="font-size: 12px"
            >{{ t('refreshdata') }}</q-tooltip>
          </q-btn>
          <q-btn
            :label="t('new')"
            icon="add"
            @click="createData()"
          >
            <q-tooltip
              class="bg-indigo"
              :offset="[10, 10]"
              content-style="font-size: 12px"
            >{{ t('new') }}</q-tooltip>
          </q-btn>
        </q-btn-group>
        <q-space />
        <q-input
          dense
          debounce="300"
          color="primary"
          v-model="search"
          @update:model-value="onRequest()"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn
          flat
          round
          dense
          :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
          @click="props.toggleFullscreen"
        />
      </template>

      <template v-slot:body-cell="props">
        <q-td :props="props">
          <div v-if="props.col.name === 'action'">
            <q-btn
              round
              flat
              icon="edit"
              @click="editData(props.rowIndex)"
            >
              <q-tooltip
                class="bg-indigo"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ t('edit') }}</q-tooltip>
            </q-btn>
            <q-btn
              round
              flat
              icon="delete_sweep"
              @click="deleteData(props.rowIndex)"
            >
              <q-tooltip
                class="bg-indigo"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ t('delete') }}</q-tooltip>
            </q-btn>
          </div>
          <div v-else>
            {{ props.value }}
          </div>
        </q-td>
      </template>

      <template v-slot:pagination>
        {{ t('total') }}{{ pagesNumber }} {{ t('page') }}
        <q-pagination
          v-model="pagination.page"
          :max="pagesNumber"
          input
          debounce="300"
          input-class="text-orange-10"
          @update:model-value="onRequest()"
        />
      </template>
    </q-table>
  </div>
  <q-dialog v-model="formData">
    <q-card style="width: 300px" class="q-px-sm q-pb-md">
      <q-card-section>
        <div class="text-h6">{{ t(`example.${mode}`) }}</div>
      </q-card-section>
      <q-item-label header>{{ t('example.value') }}</q-item-label>
      <q-card-section class="q-pt-none">
        <q-input
          dense
          v-model="data.value"
          autofocus
          @keyup.enter="submitData()"
          :rules="[val => val.length > 1 || t('example.error')]"
        /> </q-card-section>
      <q-item-label header>{{ t('example.status') }}</q-item-label>
      <q-card-section class="q-pt-none">
        <q-input
          dense
          v-model="data.status"
          @keyup.enter="submitData()"
          :rules="[val => val.length > 1 || t('example.error')]"
        /></q-card-section>
      <q-item-label header>{{ t('example.description') }}</q-item-label>
      <q-card-section class="q-pt-none">
        <q-input
          dense
          v-model="data.description"
          @keyup.enter="submitData()"
          :rules="[val => val.length > 1 || t('example.error')]"
          />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="t('cancel')" color="primary" v-close-popup @click="cancelSubmit()" />
        <q-btn flat :label="t('submit')" color="primary" v-close-popup @click="submitData(mode)" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'
import { get, post } from 'boot/axios'
import { useTokenStore } from 'stores/token'
import { useLanguageStore } from 'stores/language'
import emitter from 'boot/bus.js'

const { t } = useI18n()
const $q = useQuasar()
const tokenStore = useTokenStore()
const langStore = useLanguageStore()

const columns = computed(() => [
  { name: 'value', required: true, label: t('example.value'), align: 'left', field: 'value' },
  { name: 'status', label: t('example.status'), field: 'status' },
  { name: 'description', label: t('example.description'), field: 'description' },
  { name: 'created_time', label: t('created_time'), field: 'created_time' },
  { name: 'updated_time', label: t('updated_time'), field: 'updated_time' },
  { name: 'action', label: t('action'), align: 'right' }
])

const token = computed(() => tokenStore.token)
const rows = ref([])
const search = ref('')
const formData = ref(false)
const data = ref({})
const mode = ref('create')
const rowsCount = ref(0)

const pagination = ref({
  sortBy: 'updated_time',
  descending: false,
  page: 1,
  rowsPerPage: 30,
  rowsNumber: 30
})

const pagesNumber = computed(() => {
  if (token.value !== '') {
    return Math.ceil(rowsCount.value / pagination.value.rowsPerPage)
  } else {
    return 0
  }
})

const screenHeight = ref(`${$q.screen.height * 0.73}px`)
const screenWidth = ref(`${$q.screen.width * 0.825}px`)
const cardBackground = ref($q.dark.isActive ? '#121212' : '#ffffff')

async function onRequest(props) {
  let requestData = {}
  if (props) {
    requestData = props
  } else {
    requestData.pagination = pagination.value
  }
  await get({
    url: 'core/example/',
    params: {
      params: JSON.stringify({ data__value__icontains: search.value }),
      page: requestData.pagination.page,
      max_page: requestData.pagination.rowsPerPage
    }
  })
    .then((res) => {
      rows.value = res.results
      rowsCount.value = res.count
    })
    .catch((err) => {
      $q.notify({
        type: 'error',
        message: err
      })
      $q.loading.hide()
    }).finally(() => {
      $q.loading.hide()
    })
  pagination.value = requestData.pagination
}

function createData() {
  mode.value = 'create'
  data.value = {}
  formData.value = true
}

function editData(e) {
  mode.value = 'update'
  data.value = { ...rows.value[e] }
  formData.value = true
}

function deleteData(e) {
  mode.value = 'delete'
  data.value = { ...rows.value[e] }
  formData.value = true
}

function cancelSubmit() {
  formData.value = false
  data.value = {}
}

async function submitData(e) {
  await post(`core/example/${e}/`, data.value)
  .then(() => {
    onRequest()
    cancelSubmit()
  })
  .catch((err) => {
    $q.notify({
      type: 'error',
      message: err
    })
    $q.loading.hide()
  }).finally(() => {
    $q.loading.hide()
  })
}

onMounted(() => {
  listenToEvent()
  onRequest()
})

watch(() => $q.dark.isActive, (val) => {
  cardBackground.value = val ? '#121212' : '#ffffff'
})

function listenToEvent() {
  emitter.on('needLogin', (payload) => {
    if (payload) {
      rows.value = []
      search.value = ''
      rowsCount.value = 0
    }
  })
}

watch(() => langStore.langData, (val) => {
  if (val) {
    onRequest()
  }
})
</script>
