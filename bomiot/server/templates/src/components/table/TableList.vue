<template>
  <div class="q-pa-md">
    <q-table
      :class="$q.dark.isActive?'my-sticky-header-last-column-table-dark' : 'my-sticky-header-last-column-table'"
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
          <q-btn :label="t('new')" icon="add" @click="createUser()">
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('newUser') }}</q-tooltip>
          </q-btn>
        </q-btn-group>
        <q-space />
        <q-input dense debounce="300" color="primary" v-model="search" @input="onRequest()" @keyup.enter="onRequest()">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn
          flat round dense
          :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
          @click="props.toggleFullscreen"
        />
      </template>

      <template v-slot:body-cell="props">
        <q-td :props="props">
          <div v-if="props.col.name === 'action'">
            <q-btn round flat icon="published_with_changes" @click="changPWD(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('changepassword') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="admin_panel_settings" @click="setPermission(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('permission') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="lock_person" v-show="!props.row.is_active" @click="lockUser(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('isnotactive') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="lock_open" v-show="props.row.is_active" @click="lockUser(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('isactive') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="delete_sweep" @click="deleteUser(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('deleteuser') }}</q-tooltip>
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
import { useI18n } from "vue-i18n"
import { get, post } from 'boot/axios'
import { useTokenStore } from 'stores/token'
import { useLanguageStore } from 'stores/language'
import emitter from "boot/bus.js";

const { t } = useI18n()
const $q = useQuasar()
const tokenStore = useTokenStore()
const langStore = useLanguageStore()

const columns = computed( () => [
  {
    name: 'username', required: true, label: t('username'), align: 'left', field: 'username'},
  { name: 'email', align: 'center', label: t('email'), field: 'email' },
  { name: 'date_joined', label: t('date_joined'), field: 'date_joined' },
  { name: 'last_login', label: t('last_login'), field: 'last_login' },
  { name: 'updated_time', label: t('updated_time'), field: 'updated_time', sortable: true },
  { name: 'action', label: t('action'), align: 'right' }
])

const token = computed(() => tokenStore.token)
const rows = ref( [])
const permissionList = ref( [])
const search = ref( '')
const rowsCount = ref(0)

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
  get({
    url: 'core/user/',
    params: {
      search: search.value,
      ordering: (pagination.value.descending? '-' : '') + '' + pagination.value.sortBy,
      page: requestData.pagination.page,
      max_page: requestData.pagination.rowsPerPage
    }
  }).then(res => {
    if (!res.login) {
      rows.value = res.results
      rowsCount.value = res.count
      permissionList.value = res.permission
    }
  }).catch(err => {
    $q.loading.hide()
    return Promise.reject(err)
  })
  pagination.value = requestData.pagination
}

function createUser() {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('newUser'),
    message: t('createuser'),
    prompt: {
      model: '',
      isValid: val => val.length > 2,
      type: 'text'
    },
    cancel: true,
  }).onOk(data => {
    post('core/user/create/', {"username": data}).then(() => {
      onRequest()
    }).catch(err => {
      $q.notify({
        type: 'error',
        message: err
      })
      $q.loading.hide()
    })
  })
}

function changPWD(e) {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('changepassword'),
    message: t('changePWD'),
    prompt: {
      model: '',
      isValid: val => val.length > 2,
      type: 'text'
    },
    cancel: true,
  }).onOk(data => {
    post('core/user/changepwd/', {"id": rows.value[e].id, "pwd": data}).then(() => {
    }).catch(err => {
      $q.notify({
        type: 'error',
        message: err
      })
      $q.loading.hide()
    })
  })
}

function setPermission (e) {
  $q.dialog({
    title: t('permission'),
    message: t('choosepermission'),
    options: {
      type: 'checkbox',
      model: Object.keys(rows.value[e].permission),
      inline: true,
      items: permissionList.value
    },
    cancel: true,
  }).onOk(data => {
    post('core/user/setpermission/', {"id": rows.value[e].id, "permission": data}).then(() => {
      onRequest()
    }).catch(err => {
      $q.notify({
        type: 'error',
        message: err
      })
      $q.loading.hide()
    })
  })
}

function lockUser(e) {
  post('core/user/lock/', {"id": rows.value[e].id}).then(() => {
    onRequest()
  }).catch(err => {
    $q.notify({
      type: 'error',
      message: err
    })
    $q.loading.hide()
  })
}

function deleteUser(e) {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('deleteuser'),
    message: t('confirmnotice'),
    cancel: true,
  }).onOk(() =>{
    post('core/user/delete/', {"id": rows.value[e].id}).then(() => {
      onRequest()
    }).catch(err => {
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

watch(() => $q.dark.isActive, val => {
  CardBackground.value = val? '#121212' : '#ffffff'
})

function listenToEvent() {
  emitter.on('needLogin', (payload) => {
    if (payload) {
      rows.value = []
      permissionList.value = []
      search.value = ''
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
