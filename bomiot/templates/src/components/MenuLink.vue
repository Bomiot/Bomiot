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
  { tab: 'basic', title: t('menuLink.inscription'), icon: 'pan_tool_alt', link: '/inscription' },
  { tab: 'basic', title: 'Poetry', icon: 'img:statics/icons/poetry.png', link: '/poetry' },
  { tab: 'basic', title: 'Supervisor', icon: 'img:statics/icons/supervisor.png', link: '/supervisor' },
  { tab: 'basic', title: 'setup.ini', icon: 'psychology', link: '/setup' },
  { tab: 'basic', title: t('menuLink.terminal'), icon: 'terminal', link: '/terminal' },
  { tab: 'basic', title: 'Django', icon: 'img:statics/icons/Django.svg', link: '/django' },
  { tab: 'basic', title: 'Flask', icon: 'img:statics/icons/Flask.svg', link: '/flask_app' },
  { tab: 'basic', title: 'Fastapi', icon: 'img:statics/icons/FastAPI.svg', link: '/fastapi_app' },
  { tab: 'db', title: t('menuLink.structure'), icon: 'img:statics/icons/ros.svg', link: '/structure' },
  { tab: 'db', title: 'Sqlite', icon: 'img:statics/icons/sqlite.svg', link: '/sqlite' },
  { tab: 'db', title: 'MySQL', icon: 'img:statics/icons/mysql.svg', link: '/mysql' },
  { tab: 'db', title: 'PostgreSQL', icon: 'img:statics/icons/postgresql.svg', link: '/postgresql' },
  { tab: 'signals', title: t('menuLink.scheduler'), icon: 'access_alarm', link: '/scheduler' },
  { tab: 'signals', title: t('menuLink.observer'), icon: 'preview', link: '/observer' },
  { tab: 'signals', title: t('menuLink.server'), icon: 'storage', link: '/server' },
  { tab: 'signals', title: t('menuLink.data'), icon: 'data_object', link: '/data' },
  { tab: 'signals', title: t('menuLink.example'), icon: 'more_horiz', link: '/example' },
  { tab: 'signals', title: t('menuLink.interaction'), icon: 'handshake', link: '/interaction' },
  { tab: 'dev', title: t('menuLink.setup'), icon: 'download', link: '/dev-setup' },
  { tab: 'dev', title: t('menuLink.mainlayout'), icon: 'dashboard', link: '/dev-mainlayout' },
  { tab: 'dev', title: t('menuLink.quasarconf'), icon: 'settings', link: '/dev-quasarconf' },
  { tab: 'dev', title: t('menuLink.axios'), icon: 'api', link: '/dev-axios' },
  { tab: 'dev', title: t('menuLink.router'), icon: 'route', link: '/dev-router' },
  { tab: 'dev', title: t('menuLink.stores'), icon: 'storage', link: '/dev-stores' },
  { tab: 'dev', title: t('menuLink.project'), icon: 'dashboard_customize', link: '/dev-project' },
  { tab: 'dev', title: t('menuLink.bus'), icon: 'bolt', link: '/dev-bus' },
  { tab: 'dev', title: t('menuLink.i18n'), icon: 'translate', link: '/dev-i18n' },
  { tab: 'dev', title: t('menuLink.listcomponent'), icon: 'table_view', link: '/dev-listcomponent' },
  { tab: 'dev', title: t('menuLink.mdparser'), icon: 'description', link: '/dev-mdparser' },
  { tab: 'dev', title: t('menuLink.newpage'), icon: 'note_add', link: '/dev-newpage' },
  { tab: 'dev', title: t('menuLink.newmenu'), icon: 'playlist_add', link: '/dev-newmenu' },
  { tab: 'backend', title: t('menuLink.be_overview'), icon: 'hub', link: '/dev-be-overview' },
  { tab: 'backend', title: t('menuLink.be_setup'), icon: 'build', link: '/dev-be-setup' },
  { tab: 'backend', title: t('menuLink.be_request_flow'), icon: 'alt_route', link: '/dev-be-request-flow' },
  { tab: 'backend', title: t('menuLink.be_routes'), icon: 'share', link: '/dev-be-routes' },
  { tab: 'backend', title: t('menuLink.be_models'), icon: 'dataset', link: '/dev-be-models' },
  { tab: 'backend', title: t('menuLink.be_signal'), icon: 'cell_tower', link: '/dev-be-signal' },
  { tab: 'backend', title: t('menuLink.be_receiver'), icon: 'precision_manufacturing', link: '/dev-be-receiver' },
  { tab: 'backend', title: t('menuLink.be_jwt'), icon: 'key', link: '/dev-be-jwt' },
  { tab: 'backend', title: t('menuLink.be_department'), icon: 'admin_panel_settings', link: '/dev-be-department' },
  { tab: 'backend', title: t('menuLink.be_language'), icon: 'translate', link: '/dev-be-language' },
  { tab: 'backend', title: t('menuLink.be_scheduler'), icon: 'schedule', link: '/dev-be-scheduler' },
  { tab: 'backend', title: t('menuLink.be_newmodule'), icon: 'add_box', link: '/dev-be-newmodule' },
  { tab: 'cli', title: t('menuLink.cli_project'), icon: 'create_new_folder', link: '/dev-cli-project' },
  { tab: 'cli', title: t('menuLink.cli_app'), icon: 'apps', link: '/dev-cli-app' },
  { tab: 'cli', title: t('menuLink.cli_api'), icon: 'api', link: '/dev-cli-api' },
  { tab: 'cli', title: t('menuLink.cli_deploy'), icon: 'rocket_launch', link: '/dev-cli-deploy' },
  { tab: 'cli', title: t('menuLink.cli_init'), icon: 'play_arrow', link: '/dev-cli-init' },
  { tab: 'cli', title: t('menuLink.cli_initadmin'), icon: 'person_add', link: '/dev-cli-initadmin' },
  { tab: 'cli', title: t('menuLink.cli_initpwd'), icon: 'lock_reset', link: '/dev-cli-initpwd' },
  { tab: 'cli', title: t('menuLink.cli_migrate'), icon: 'storage', link: '/dev-cli-migrate' },
  { tab: 'cli', title: t('menuLink.cli_makemigrations'), icon: 'note_add', link: '/dev-cli-makemigrations' },
  { tab: 'cli', title: t('menuLink.cli_loaddata'), icon: 'upload', link: '/dev-cli-loaddata' },
  { tab: 'cli', title: t('menuLink.cli_dumpdata'), icon: 'download', link: '/dev-cli-dumpdata' },
  { tab: 'cli', title: t('menuLink.cli_run'), icon: 'terminal', link: '/dev-cli-run' },
  { tab: 'sponsor', title: t('menuLink.sponsor_build'), icon: 'build_circle', link: '/dev-BUILD_FLOW' },
  { tab: 'sponsor', title: t('menuLink.sponsor_update'), icon: 'system_update', link: '/dev-AUTO_UPDATE' },
  { tab: 'sponsor', title: t('menuLink.sponsor_authkey'), icon: 'vpn_key', link: '/dev-auth_key' },
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
  router.push(e.routerTo).catch(err => {
    if (err.name !== 'NavigationDuplicated') {
      console.log('[MenuLink] push error:', err.name, err.message)
    }
  })
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
