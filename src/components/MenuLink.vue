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
  { tab: 'test1', title: t('menuTab.home'), icon: 'home', link: '/' },
  { tab: 'test1', title: t('menuLink.test1'), icon: 'looks_one', link: '/md/test1' },
  { tab: 'test2', title: t('menuLink.test1'), icon: 'repeat_one', link: '/md/test1' },
  { tab: 'test2', title: t('menuLink.test2'), icon: 'looks_two', link: '/md/test2' }
])


function menuChange (e) {
    if (e.link.split('/')[1] === 'md') {
      e.routerTo = e.link + '/' + langStore.langData
    } else {
      e.routerTo = e.link
    }
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
  menuLinks.value.some(item =>{
    if (menuStore.menuData.link === item.link) {
      menuChange(menuStore.menuData)
      return true
    }
  })
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
