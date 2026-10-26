<template>
  <q-page class="flex flex-center">
    <div id="lottie" style="width: 80%; max-width: 60%"></div>
  </q-page>
</template>

<script setup>
import { onMounted, ref, computed, nextTick, onUnmounted } from 'vue'
import welcome from 'components/lottie/welcome.json'
import { useMeta } from "quasar"
import { useI18n } from "vue-i18n"

const { t } = useI18n()
const animation = ref(null)
const lottieModule = ref(null)

const title = computed(()=> { return t('title') })
const description = computed(()=> { return t('description') })
const keywords = computed(()=> { return t('keywords') })

async function initLottie () {
  if (!lottieModule.value) {
    try {
      lottieModule.value = await import('lottie-web');
    } catch (error) {
      console.error("Failed to load lottie-web:", error);
      return
    }
  }

  await nextTick();
  const container = document.getElementById("lottie");
  if (container && lottieModule.value) {
    animation.value = lottieModule.value.loadAnimation({
      container: container,
      renderer: "svg",
      loop: true,
      autoplay: true,
      animationData: welcome
    });
    lottieModule.value.setSpeed(1.5)
  }
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

onUnmounted(() => {
  if (animation.value) {
    animation.value.destroy();
  }
})
</script>