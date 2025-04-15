<template>
  <q-page class="flex flex-center">
    <div id="lottie" style="width: 80%; max-width: 60%"></div>
  </q-page>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import lottie from 'lottie-web'
import welcome from 'components/lottie/welcome.json'
import { useMeta } from "quasar"
import { useI18n } from "vue-i18n"


const { t } = useI18n()
const animation = ref(null)

const title = computed(()=> { return t('title') })
const description = computed(()=> { return t('description') })
const keywords = computed(()=> { return t('keywords') })

function initLottie () {
  animation.value = lottie.loadAnimation({
    container: document.getElementById("lottie"),
    renderer: "svg",
    loop: true,
    autoplay: true,
    animationData: welcome
  });
  lottie.setSpeed(1.5)
}

useMeta(() => {
  return {
    title: title.value,
    meta: {
        description: { name: 'description', content: description.value },
        keywords: { name: 'keywords', content: keywords.value },
      }
    }
  })


onMounted (() => {
  initLottie()
})


</script>
