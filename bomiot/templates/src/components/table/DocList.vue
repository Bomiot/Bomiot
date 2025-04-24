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
            <q-btn round flat icon="visibility" @click="previewImg(props.rowIndex)" v-show="isImg(props.row)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('doc.download') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="cloud_download" @click="downloadFile(props.rowIndex)" v-show="!isImg(props.row)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('doc.download') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="share" @click="shareFile(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('doc.shared_to') }}</q-tooltip>
            </q-btn>
            <q-btn round flat icon="delete_sweep" @click="deleteFile(props.rowIndex)">
              <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('deletefile') }}</q-tooltip>
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
    name: 'name', required: true, label: t('doc.name'), align: 'left', field: 'name'},
  { name: 'type', align: 'center', label: t('doc.type'), field: 'type' },
  { name: 'size', align: 'center' ,label: t('doc.size'), field: 'size' },
  { name: 'owner', align: 'center', label: t('doc.owner'), field: 'owner' },
  { name: 'created_time', align: 'center', label: t('created_time'), field: 'created_time', sortable: true },
  { name: 'updated_time', align: 'center', label: t('updated_time'), field: 'updated_time', sortable: true },
  { name: 'action', label: t('action'), align: 'right' }
])

const token = computed(() => tokenStore.token)
const rows = ref( [])
const userList = ref( [])
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
    url: 'core/user/files/',
    params: {
      search: search.value,
      ordering: (pagination.value.descending? '-' : '') + '' + pagination.value.sortBy,
      page: requestData.pagination.page,
      max_page: requestData.pagination.rowsPerPage
    }
  }).then(res => {
    rows.value = res.results
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

function downloadFile(e) {
  fetch('media/' + tokenStore.tokenDataGet.username + '/' + rows.value[e].name)
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok.');
      return response.blob();
    })
    .then(blob => {
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = rows.value[e].name;
      link.click();
    })
    .catch(err => {
      $q.notify({
        type: 'error',
        message: err
      })
    });
}

function shareFile (e) {
  var model_data = []
  userList.value.forEach(item => {
  model_data.push({
      label: item.toString().split(',')[1],
      value: item.toString().split(',')[0]
    })
  })
  $q.dialog({
    title: t('doc.share'),
    message: t('doc.shared_to'),
    options: {
      type: 'checkbox',
      model: model_data,
      inline: true,
      items: userList.value
    },
    cancel: true,
  }).onOk(data => {
    post('core/user/files/share/', {"id": rows.value[e].id, "users": data}).then(() => {
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

function isImg(e) {
  console.log(e)
  const list = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp', 'svg', 'psd', 'raw', 'tga', 'ico']
  return list.includes(e.type)
}

function previewImg(e) {
  $q.dialog({
    title: rows.value[e].name,
    message: `<img src="media/${tokenStore.tokenDataGet.username}/${rows.value[e].name}" style="max-height: ${ScreenHeight.value}; width: 100%">`,
    html: true
  })
}

function deleteFile(e) {
  $q.dialog({
    dark: $q.dark.isActive,
    title: t('deletefile'),
    message: t('deletefilenotice'),
    cancel: true,
  }).onOk(() =>{
    post('core/user/file/delete/', {"id": rows.value[e].id}).then(() => {
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
      userList.value = []
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
