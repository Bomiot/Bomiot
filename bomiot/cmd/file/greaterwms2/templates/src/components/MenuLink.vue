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
  { tab: 'guide', title: t('menuLink.home'), icon: 'home', link: '/' },
  { tab: 'guide', title: t('menuLink.why_greaterwms'), icon: 'live_help', link: '/md/why_greaterwms' },
  { tab: 'guide', title: t('menuLink.sponsors_and_supporters'), icon: 'stress_management', link: '/md/sponsors_and_supporters' },
  { tab: 'guide', title: t('menuLink.why_donate'), icon: 'bloodtype', link: '/md/why_donate' },
  { tab: 'guide', title: t('menuLink.please_dont_do_that'), icon: 'do_not_touch', link: '/md/please_dont_do_that' },
  { tab: 'deploy', title: t('menuLink.software_version_requirements'), icon: 'terminal', link: '/md/software_version_requirements' },
  { tab: 'deploy', title: t('menuLink.server_configuration_recommendations'), icon: 'dns', link: '/md/server_configuration_recommendations' },
  { tab: 'deploy', title: t('menuLink.win_10'), icon: 'laptop_windows', link: '/md/win_10' },
  { tab: 'deploy', title: t('menuLink.centos7_x64_bit'), icon: 'link', link: '/md/centos_7' },
  { tab: 'deploy', title: t('menuLink.ubuntu20_x64'), icon: 'link', link: '/md/ubuntu_20' },
  { tab: 'deploy', title: t('menuLink.ios_environment'), icon: 'tablet_mac', link: '/md/ios_environment' },
  { tab: 'deploy', title: t('menuLink.android_environment'), icon: 'phone_android', link: '/md/android_environment' },
  { tab: 'deploy', title: t('menuLink.android_sign'), icon: 'view_carousel', link: '/md/android_sign' },
  { tab: 'deploy', title: t('menuLink.quasar_framework'), icon: 'public', link: '/md/quasar' },
  { tab: 'deploy', title: t('menuLink.supervisor_process_guarded'), icon: 'supervised_user_circle', link: '/md/supervisor_process_guarded' },
  { tab: 'deploy', title: t('menuLink.docker_deployment'), icon: 'link', link: '/md/docker_deployment' },
  { tab: 'deploy', title: t('menuLink.nginx_config'), icon: 'link', link: '/md/nginx_config' },
  { tab: 'deploy', title: t('menuLink.nas'), icon: 'share', link: '/md/nas' },
  { tab: 'download', title: t('menuLink.windows'), icon: 'laptop_windows', link: '/md/windows' },
  { tab: 'download', title: t('menuLink.ios'), icon: 'tablet_mac', link: '/md/ios' },
  { tab: 'download', title: t('menuLink.android'), icon: 'phone_android', link: '/md/android' },
  { tab: 'operation', title: t('menuLink.web'), icon: 'computer', link: '/md/web_operation' },
  { tab: 'operation', title: t('menuLink.app'), icon: 'phone_iphone', link: '/md/app_operation' },
  { tab: 'product', title: t('menuLink.greaterwms'), icon: 'settings_system_daydream', link: '/md/greaterwms' },
  { tab: 'product', title: t('menuLink.smart_bi'), icon: 'receipt_long', link: '/md/bi' },
  { tab: 'product', title: t('menuLink.wcs'), icon: 'precision_manufacturing', link: '/md/wcs' },
  { tab: 'contact', title: t('menuLink.contact'), icon: 'contact_mail', link: '/md/contact_us' },
])

function menuChange (e) {
  const item = { ...e }
  if (item.link.startsWith('/md/')) {
    item.routerTo = item.link + '/' + langStore.langGet
  } else {
    item.routerTo = item.link
  }
  menuLinks.value.some(item => {
    if (item.link === '/') {
      item.routerTo = '/'
      menuStore.homePage(item)
      return true
    }
  })
  menuStore.menuDataChange(item)
  router.push(item.routerTo)
}

onMounted(() => {
  if (menuStore.menuData.routerTo) {
    router.push(menuStore.menuData.routerTo)
  }
})


watch(() => langStore.langData, val => {
  if (val) {
    menuLinks.value.some(item => {
      if (menuStore.menuData.link === item.link) {
        menuChange(menuStore.menuData)
        return true
      }
    })
  }
})


watch(() => tabStore.tabData, val => {
  menuLinks.value.some(item => {
    if (val === item.tab) {
      menuChange(item)
      return true
    }
  })
})

</script>
