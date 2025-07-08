<template>
  <q-item
    v-for="(list, index) in menuLinks"
    v-show="list.tab === tabStore.tabData"
    :key="index"
    v-bind="list"
    clickable
    @click="menuChange(list)"
    :active="list.link === menuStore.menuData.link"
  >
    <q-item-section
      v-if="list.icon"
      avatar
    >
      <q-icon :name="list.icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ list.title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useI18n } from "vue-i18n"
import { useTabDataStore } from 'stores/tab'
import { useLanguageStore } from "stores/language"
import { useMenuDataStore } from "stores/menu"
import { useRouter } from 'vue-router'


const { t } = useI18n()
const router = useRouter()
const tabStore = useTabDataStore()
const langStore = useLanguageStore()
const menuStore = useMenuDataStore()


const menuLinks = computed(() => [
  { tab: 'standard', title: t('menuLink.home'), icon: 'home', link: '/' },
  { tab: 'standard', title: t('menuLink.user'), icon: 'people', link: '/user' },
  { tab: 'standard', title: t('menuLink.team'), icon: 'diversity_3', link: '/team' },
  { tab: 'standard', title: t('menuLink.department'), icon: 'diversity_2', link: '/department' },
  { tab: 'standard', title: t('upload.center'), icon: 'upload', link: '/upload' },
  { tab: 'standard', title: t('doc.center'), icon: 'download', link: '/doc' },
  { tab: 'standard', title: 'PyPi', icon: 'cloud_sync', link: '/pypi' },
  { tab: 'standard', title: 'PyPi Stats', icon: 'pie_chart', link: '/pypicharts' },
  { tab: 'server', title: 'PID', icon: 'account_tree', link: '/pid' },
  { tab: 'server', title: 'CPU', icon: 'select_all', link: '/cpu' },
  { tab: 'server', title: 'Memory', icon: 'memory', link: '/memory' },
  { tab: 'server', title: 'Disk', icon: 'storage', link: '/disk' },
  { tab: 'server', title: 'Network', icon: 'wifi', link: '/network' },
  { tab: 'server', title: 'DashBoard', icon: 'dashboard', link: '/serverecharts' },
  { tab: 'server', title: 'PID Tree', icon: 'view_quilt', link: '/pidcharts' },
  { tab: 'api', title: 'API', icon: 'api', link: '/api' },
  { tab: 'api', title: t('menuLink.example'), icon: 'more_horiz', link: '/example' },
  { tab: 'basic', title: 'README', icon: 'img:icons/logo.png', link: '/readme' },
  { tab: 'basic', title: 'Locust', icon: 'img:statics/icons/locust.png', link: '/locust' },
  { tab: 'basic', title: 'Poetry', icon: 'img:statics/icons/poetry.png', link: '/poetry' },
  { tab: 'basic', title: 'Supervisor', icon: 'img:statics/icons/supervisor.png', link: '/supervisor' },
  { tab: 'db', title: 'Sqlite', icon: 'img:statics/icons/sqlite.svg', link: '/sqlite' },
  { tab: 'db', title: 'MySQL', icon: 'img:statics/icons/mysql.svg', link: '/mysql' },
  { tab: 'db', title: 'PostgreSQL', icon: 'img:statics/icons/postgresql.svg', link: '/postgresql' },
])

function menuChange (e) {
  e.routerTo = e.link
  menuLinks.value.some(item =>{
    if (item.link === '/') {
      item.routerTo = '/'
      menuStore.homePage(item)
      return true
    }
  })
  menuStore.menuDataChange(e)
  router.push(e.routerTo)
}

onMounted(() => {
  router.push(menuStore.menuData.routerTo)
})


watch(() => langStore.langData, val => {
  if (val) {
   menuLinks.value.some(item =>{
    if (menuStore.menuData.link === item.link) {
      menuChange(menuStore.menuData)
        return true
      }
    })
  }
})


watch(() => tabStore.tabData, val => {
  menuLinks.value.some(item =>{
    if (val === item.tab) {
      menuChange(item)
      return true
    }
  })
})

</script>
