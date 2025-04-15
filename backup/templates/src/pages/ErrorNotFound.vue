<template>
  <div class="fullscreen bg-blue text-white text-center q-pa-md flex flex-center">
      <div id="lottie" style="width: 60%; max-width: 90%; height: 60%"></div>
      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="blue"
        unelevated
        :label="t('gohome')"
        no-caps
        @click="goHome()"
      />
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import lottie from 'lottie-web'
import error404 from 'components/lottie/404.json'
import { useRouter } from 'vue-router'
import { useMenuDataStore } from "stores/menu"
import { useTabDataStore } from 'stores/tab'
import { useI18n } from "vue-i18n"


const { t } = useI18n()
const animation = ref(null)
const router = useRouter()
const menuStore = useMenuDataStore()
const tabStore = useTabDataStore()


function initLottie () {
  animation.value = lottie.loadAnimation({
    container: document.getElementById("lottie"),
    renderer: "svg",
    loop: true,
    autoplay: true,
    animationData: error404
  });
  lottie.setSpeed(2.5)
}


function menuChange (e) {
  tabStore.tabDataChange(e.tab)
  menuStore.menuDataChange(e)
  router.push(e.routerTo)
}

function goHome() {
  menuChange(menuStore.homeData)
}

onMounted (() => {
  initLottie()
})


</script>
