<template>
  <q-layout view="hHh lpR fFf">
    <q-header :class="{'bg-grey-10': $q.dark.isActive, 'main-headers-sun': !$q.dark.isActive}">
      <transition
        appear
        enter-active-class="animated fadeIn slower delay-10s"
        leave-active-class="animated fadeOut slower delay-10s">
      <q-toolbar>
        <q-btn dense flat round icon="menu" v-show="leftDrawerStore.leftDrawerMenu" @click="leftDrawerStore.toggleleftDrawer" />
        <q-toolbar-title @click="$router.push('/')">
          <q-avatar>
            <img src="/icons/logo.png" :alt="appNameStore.appName + ' Logo'" />
          </q-avatar>
            {{ appNameStore.appName }} Team©
        </q-toolbar-title>
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
        <q-btn-group unelevated style="margin-left: 25px">
          <q-btn v-show="tokenStore.token === ''" :label="t('login')" @click="loginForm = true"/>
          <q-btn v-show="tokenStore.token !== ''" :label="t('logout')" @click="logOuts()"/>
        </q-btn-group>
        <q-btn dense flat round icon="menu" v-show="rightDrawerStore.rightDrawerMenu" @click="rightDrawerStore.toggleRightDrawer" />
      </q-toolbar>
      </transition>
      <TabList />
    </q-header>

    <q-drawer
      v-model="leftDrawerStore.leftDrawerOpen"
      side="left"
      :breakpoint="500"
      :class="{'drawer-background-dark text-white': $q.dark.isActive}">
        <q-list padding>
          <MenuLink />
        </q-list>
    </q-drawer>

    <q-drawer :class="{'drawer-background-dark': $q.dark.isActive}" v-model="rightDrawerStore.rightDrawerOpen" side="right" style="width: 310px!important">

    </q-drawer>

    <q-page-container>
        <router-view />
        <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
          <q-btn fab icon="keyboard_arrow_up" color="indigo"></q-btn>
        </q-page-scroller>
    </q-page-container>
  </q-layout>
  <q-dialog v-model="loginForm">
    <q-card style="min-width: 350px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ t('login') }}</div>
        <q-space />
        <q-btn icon="close" @click="cancelLogin()" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section>
        <q-input autofocus :label="t('username')" v-model="loginData.username"></q-input>
        <q-input :label="t('password')" v-model="loginData.password"></q-input>
      </q-card-section>
      <q-card-actions align="right" class="text-primary">
        <q-btn flat :label="t('cancel')" @click="cancelLogin()" v-close-popup />
        <q-btn flat :label="t('submit')" @click="submitLogin()" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>


<script setup>
import { onMounted, computed, ref } from 'vue'
import { useAppNameStore } from 'stores/appName'
import { userightDrawerStore } from "stores/rightDrawer"
import { useleftDrawerStore } from "stores/leftDrawer"
import { useLanguageStore } from 'stores/language'
import { useTokenStore } from "stores/token"
import { useI18n } from "vue-i18n"
import { useQuasar } from "quasar"
import { useRouter } from 'vue-router'
import { openURL } from 'quasar'
import { post } from 'boot/axios'
import DarkMode from 'components/dark/DarkMode.vue'
import LangChoice from 'components/lang/LangChoice.vue'
import TabList from 'components/TabList.vue'
import MenuLink from 'components/MenuLink.vue'


const { t } = useI18n()
const $q = useQuasar()
const $router = useRouter()
const appNameStore = useAppNameStore()
const rightDrawerStore = userightDrawerStore()
const leftDrawerStore = useleftDrawerStore()
const langStore = useLanguageStore()
const tokenStore = useTokenStore()

const loginForm = ref(false)
const loginData = ref({
  username: '',
  password: ''
})

const lang = computed(() => langStore.langData)

function cancelLogin () {
  loginData.value = {
    username: '',
    password: ''
  }
}

function submitLogin () {
  if (loginData.value.username !== '' && loginData.value.password !== '') {
    post('login/', loginData.value).then((res) =>{
      if (res.token) {
        tokenStore.tokenChange(res.token)
      } else {
        tokenStore.tokenChange('')
      }
      cancelLogin()
    }).catch((err) =>{
      console.log(err)
    })
  } else {
    $q.notify({
      type: 'warning',
      message: t('usererror')
    })
  }
}

function logOuts () {
  tokenStore.tokenChange('')
  $q.notify({
      type: 'info',
      message: t('logoutnotice')
    })
}

function openLink (e) {
  openURL(e)
}

onMounted(() => {
  tokenStore.tokenCheck()
})

</script>

