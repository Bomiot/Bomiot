<template>
    <div class="q-pa-md">
      <div v-html="tocRouter" style="margin-top: 25px; width: 99%; max-width: 99%"></div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMDDataStore } from "stores/mdDocs"
import { useMenuDataStore } from "stores/menu"


const mdStore = useMDDataStore()
const menuStore = useMenuDataStore()

const tocRouter = computed(() => mdStore.tocRouter)

</script>

