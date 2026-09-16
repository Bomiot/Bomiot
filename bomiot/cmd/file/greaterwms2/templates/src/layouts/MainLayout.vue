<template>
  <q-layout view="hHh lpR fFf">
    <q-header :class="[$q.dark.isActive ? 'bg-grey-10' : 'main-headers-sun']">
      <q-toolbar>
        <q-btn dense flat round icon="menu" style="display:none;" />
        <q-toolbar-title @click="$router.push('/')">
          <q-avatar>
            <img src="/icons/logo.png" :alt="appNameStore.appName + ' Logo'" />
          </q-avatar>
            {{ appNameStore.appName }} Team©
        </q-toolbar-title>
        <q-space />
        <div>
          <q-select
            v-model="projectData"
            :options="projectOptions"
            stack-label
            borderless
            dark
            @update:model-value="projectChange($event)"
          >
            <template v-slot:selected>
              {{ $t('project') }}
              <q-chip
                v-if="projectData"
                dense
                square
                color="white"
                text-color="primary"
                class="q-my-none q-ml-xs q-mr-none"
              >
                {{ projectData.label }}
              </q-chip>
              <q-badge v-else>*none*</q-badge>
            </template>
          </q-select>
        </div>
        <q-btn dense flat round style="margin-right: 10px" @click="openLink('https://space.bilibili.com/407321291')">
          <img src="/statics/icons/bilibili.svg" style="width: 25px" :alt="appNameStore.appName + ' Bilibili'"/>
          <q-tooltip class="bg-indigo" :offset="[15, 15]" content-style="font-size: 12px">
            Bilibili
          </q-tooltip>
        </q-btn>
        <q-btn dense flat round style="margin-right: 10px" @click="openLink('https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA')">
          <img src="/statics/icons/youtube.svg" style="width: 25px" :alt="appNameStore.appName + ' YouTube'" />
          <q-tooltip class="bg-indigo" :offset="[15, 15]" content-style="font-size: 12px">
            YouTube
          </q-tooltip>
        </q-btn>
        <q-btn dense flat round style="margin-right: 10px" @click="openLink('https://gitee.com/Bomiot/Bomiot')">
          <img src="/statics/icons/gitee.svg" style="width: 25px" :alt="appNameStore.appName + ' Gitee'" />
          <q-tooltip class="bg-indigo" :offset="[15, 15]" content-style="font-size: 12px">
            Gitee
          </q-tooltip>
        </q-btn>
        <q-btn dense flat round @click="openLink('https://github.com/Bomiot/Bomiot')">
          <img src="/statics/icons/github.svg" style="width: 25px" :alt="appNameStore.appName + ' GitHub'" />
          <q-tooltip class="bg-indigo" :offset="[15, 15]" content-style="font-size: 12px">
            GitHub
          </q-tooltip>
        </q-btn>
        <LangChoice />
        <DarkMode />
      </q-toolbar>
      <TabList />
    </q-header>

    <q-drawer
      v-model="leftDrawerStore.leftDrawerOpen"
      side="left"
      :width="300"
      :breakpoint="500"
      :class="{'drawer-background-dark text-white': $q.dark.isActive}">
        <q-list padding>
          <MenuLink />
        </q-list>
    </q-drawer>

    <q-page-container>
        <router-view />
        <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
          <q-btn fab icon="keyboard_arrow_up" color="indigo"></q-btn>
        </q-page-scroller>
    </q-page-container>
  </q-layout>
</template>


<script setup>
import { onMounted, ref, toRaw, watch } from 'vue'
import { useAppNameStore } from 'stores/appName'
import { useleftDrawerStore } from "stores/leftDrawer"
import { useProjectStore } from 'stores/project'
import { useQuasar, openURL } from "quasar"
import { useRouter } from 'vue-router'
import { get } from 'boot/axios'
import DarkMode from 'components/dark/DarkMode.vue'
import LangChoice from 'components/lang/LangChoice.vue'
import TabList from 'components/TabList.vue'
import MenuLink from 'components/MenuLink.vue'

const $q = useQuasar()
const $router = useRouter()
const appNameStore = useAppNameStore()
const leftDrawerStore = useleftDrawerStore()
const projectStore = useProjectStore()

const projectData = ref({})
const projectOptions = ref([])

function openLink (e) {
  openURL(e)
}

function projectChange (e) {
  let rawData = toRaw(e)
  projectStore.projectChange(rawData.value)
}

async function getProjectList () {
  await get({
    url: 'projectlist/',
    params: {}
  })
    .then((res) => {
      projectOptions.value = res.list
      projectCheck()
    })
    .catch((err) => {
      console.log(err)
    })
}

function projectCheck () {
  for (let item of projectOptions.value) {
    if (item.value === projectStore.projectDataGet) {
      projectData.value = item
    }
  }
}

watch(() => projectStore.project, val => {
  if (val) {
    console.log('Project changed:', val)
    $q.cookies.set('project', val)
    window.location.href = '/'
  }
})

onMounted(() => {
  // Sync project from cookie to store on startup
  const cookieProject = $q.cookies.get('project')
  if (cookieProject && cookieProject !== projectStore.project) {
    projectStore.projectChange(cookieProject)
  } else if (!cookieProject) {
    $q.cookies.set('project', projectStore.project)
  }
  getProjectList()
})
</script>
