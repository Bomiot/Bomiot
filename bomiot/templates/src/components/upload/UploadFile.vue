<template>
  <div class="q-pa-md">
      <q-uploader
        ref="uploaderRef"
        :url="getUrl"
        label="Individual upload"
        :headers="[{name: 'token', value: token}, {name: 'language', value: lang}]"
        multiple
        :style="{ height: ScreenHeight, width: ScreenWidth, maxHeight: ScreenHeight }"
        @uploaded="onUploaded"
        @error="onError"
      >
      <template v-slot:header="scope">
        <div class="row no-wrap items-center q-pa-sm q-gutter-xs" :style="{ backgroundColor: CardBackground }">
          <q-btn v-if="scope.queuedFiles.length > 0" icon="clear" @click="scope.removeQueuedFiles" round dense flat >
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.clear') }}</q-tooltip>
          </q-btn>
          <q-btn v-if="scope.uploadedFiles.length > 0" icon="done_all" @click="scope.removeUploadedFiles" round dense flat >
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.remove') }}</q-tooltip>
          </q-btn>
          <q-spinner v-if="scope.isUploading" class="q-uploader__spinner" />
          <div class="col">
            <div class="q-uploader__title">{{ t('upload.choose') }}</div>
            <div class="q-uploader__subtitle">{{ scope.uploadSizeLabel }} / {{ scope.uploadProgressLabel }}</div>
          </div>
          <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" @click="scope.pickFiles" round dense flat>
            <q-uploader-add-trigger />
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.add') }}</q-tooltip>
          </q-btn>
          <q-btn v-if="scope.canUpload" icon="cloud_upload" @click="scope.upload" round dense flat >
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.server') }}</q-tooltip>
          </q-btn>
          <q-btn v-if="scope.isUploading" icon="stop_circle" @click="scope.abort" round dense flat >
            <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.abort') }}</q-tooltip>
          </q-btn>
        </div>
      </template>

      <template v-slot:list="scope">
        <q-list separator>
          <q-item v-for="file in scope.files" :key="file.__key">
            <q-item-section>
              <q-item-label class="full-width ellipsis">
                {{ file.name }}
              </q-item-label>
              <q-item-label caption>
                <p v-if="file.__status === 'idle'">
                  {{ t('upload.status') }} {{ t('upload.idle') }}
                </p>
                <p v-else-if="file.__status === 'uploaded'" style="background: green; color: white">
                  {{ t('upload.status') }} {{ file.notice }}
                </p>
                <p v-else style="background: red; color: white">
                  {{ t('upload.status') }} {{ file.notice }}
                </p>
              </q-item-label>

              <q-item-label caption>
                {{ file.__sizeLabel }} / {{ file.__progressLabel }}
              </q-item-label>
            </q-item-section>

            <q-item-section
              v-if="file.__img"
              thumbnail
              class="gt-xs"
            >
              <img :src="file.__img.src" @click="imgShow(file)">
            </q-item-section>

            <q-item-section top side>
              <q-btn
                v-if="$q.dark.isActive"
                class="gt-xs"
                size="12px"
                flat
                dense
                round
                icon="delete"
                color="white"
                @click="scope.removeFile(file)"
              >
                <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.delete') }}</q-tooltip>
              </q-btn>
              <q-btn
                v-else
                class="gt-xs"
                size="12px"
                flat
                dense
                round
                icon="delete"
                color="black"
                @click="scope.removeFile(file)"
              >
                <q-tooltip class="bg-indigo" :offset="[10, 10]" content-style="font-size: 12px">{{ t('upload.delete') }}</q-tooltip>
              </q-btn>
            </q-item-section>
          </q-item>

        </q-list>
      </template>
    </q-uploader>
  </div>
</template>

<script setup>
import { useQuasar } from 'quasar'
import { useI18n } from "vue-i18n"
import { useTokenStore } from 'stores/token'
import { useLanguageStore } from 'stores/language'
import { computed, ref, watch } from "vue"
import { baseURL } from 'boot/axios'

const { t } = useI18n()
const $q = useQuasar()
const tokenStore = useTokenStore()
const langStore = useLanguageStore()

const uploaderRef = ref(null)

const token = computed(() => tokenStore.token)
const lang = computed(() => langStore.langGet)

const ScreenHeight = ref($q.screen.height * 0.85 + '' + 'px')
const ScreenWidth = ref($q.screen.width * 0.825 + '' + 'px')
const CardBackground = ref($q.dark.isActive? '#1D1D1D' : '#1972D2')

function onUploaded(response) {
  if (JSON.parse(response.xhr.responseText).msg) {
    uploaderRef.value.files.forEach(item => {
      if (item.name === response.files[0].name) {
        item.notice = JSON.parse(response.xhr.responseText).msg
        item.__status = 'uploaded'
      }
    })
  }
  if (JSON.parse(response.xhr.responseText).detail) {
    uploaderRef.value.files.forEach(item => {
      if (item.name === response.files[0].name) {
        item.notice = JSON.parse(response.xhr.responseText).detail
        item.__status = 'failed '
      }
    })
  }
}

function onError(error) {
  console.error('Upload error:', error)
}

function getUrl (e) {
  if (e) {
    var domain = window.location.hostname;
    if (domain === 'localhost') {
      return `${baseURL}/core/user/upload/`
    } else {
      return 'core/user/upload/'
    }
  }
}

function imgShow(e) {
  $q.dialog({
      message: `<img src="${e.__img.src}" style="max-height: ${ScreenHeight.value}; width: 100%">`,
      html: true
    })
}

watch(() => $q.dark.isActive, val => {
  CardBackground.value = val? '#1D1D1D' : '#1972D2'
})

</script>
