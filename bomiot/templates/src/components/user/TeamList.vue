
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
      :rows-per-page-options="[1, 30, 50, 200, 1000]"
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
            @click="createTeam()"
          >
            <q-tooltip
              class="bg-indigo"
              :offset="[10, 10]"
              content-style="font-size: 12px"
            >{{ t('team.new') }}</q-tooltip>
          </q-btn>
        </q-btn-group>
        <q-space />
        <q-input
          dense
          debounce="300"
          color="primary"
          v-model="search"
          @input="onRequest()"
          @keyup.enter="onRequest()"
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
              @click="changTeam(props.rowIndex)"
            >
              <q-tooltip
                class="bg-indigo"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ t('team.change') }}</q-tooltip>
            </q-btn>
            <q-btn
              round
              flat
              icon="delete_sweep"
              @click="deleteTeam(props.rowIndex)"
            >
              <q-tooltip
                class="bg-indigo"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ t('team.delete') }}</q-tooltip>
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
          input-class="text-orange-10"
          @update:model-value="onRequest()"
        />
      </template>
    </q-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'
import { get, post } from 'boot/axios'
import { useTokenStore } from 'stores/token'
import { useLanguageStore } from 'stores/language'
import { usePermissionStore } from 'stores/permission'
import emitter from 'boot/bus.js'

const { t } = useI18n()
const $q = useQuasar()
const tokenStore = useTokenStore()
const langStore = useLanguageStore()
const permissionList = usePermissionStore()

const columns = computed(() => [
  {
    name: 'name',
    required: true,
    label: t('team.name'),
    align: 'left',
    field: 'name'
  },
  { name: 'created_time', label: t('created_time'), field: 'created_time' },
  { name: 'updated_time', label: t('updated_time'), field: 'updated_time' },
  { name: 'action', label: t('action'), align: 'right' }
])

const token = computed(() => tokenStore.token)
const rows = ref([])
const search = ref('')
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

function onRequest(props) {
  let requestData = {}
  if (props) {
    requestData = props
  } else {
    requestData.pagination = pagination.value
  }
  get({
    url: 'core/team/',
    params: {
      search: search.value,
      page: requestData.pagination.page,
      max_page: requestData.pagination.rowsPerPage
    }
  })
    .then((res) => {
      rows.value = res.results
      rowsCount.value = res.count
      permissionList.permissionChange(res.permission_list)
    })
    .catch((err) => {
      $q.notify({
        type: 'error',
        message: err
      })
      $q.loading.hide()
    })
  pagination.value = requestData.pagination
}

function createTeam() {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('team.new'),
    message: t('team.create'),
    prompt: {
      model: '',
      isValid: (val) => val.length > 2,
      type: 'text'
    },
    cancel: true
  })
    .onOk(async (data) => {
      await post('core/team/create/', { name: data })
        .then(() => {
          onRequest()
        })
        .catch((err) => {
          $q.notify({
            type: 'error',
            message: err
          })
          $q.loading.hide()
        })
    })
}

function changTeam(e) {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('team.change'),
    message: t('team.changeteam'),
    prompt: {
      model: '',
      isValid: (val) => val.length > 2,
      type: 'text'
    },
    cancel: true
  })
    .onOk(async (data) => {
      await post('core/team/change/', { id: rows.value[e].id, name: data })
        .then(() => {
          onRequest()
        })
        .catch((err) => {
          $q.notify({
            type: 'error',
            message: err
          })
          $q.loading.hide()
        })
    })
}

function deleteTeam(e) {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('team.delete'),
    message: t('confirmnotice'),
    cancel: true
  })
    .onOk(async () => {
      await post('core/team/delete/', { id: rows.value[e].id })
        .then(() => {
          onRequest()
        })
        .catch((err) => {
          $q.notify({
            type: 'error',
            message: err
          })
          $q.loading.hide()
        })
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
