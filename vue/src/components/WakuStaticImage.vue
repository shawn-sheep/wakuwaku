<template>
  <div ref="containerRef" style="width: 100%;position: relative" :style="{height: containerHeight + 'px'}">
    <div style="position: absolute; width: 100%; height: 100%"></div>
    <img style="width: 100%" :src="props.img.src">
  </div>
</template>

<script setup lang="ts">
import {image} from "@/assets/js/api";
import {onMounted, reactive, ref, watch} from "vue";

// eslint-disable-next-line no-undef
const props = defineProps<{
  img : image
}>()

const containerRef = ref<Element>()
const containerHeight = ref<number>(0)

onMounted(() => {
  watch(
      () => props.img,
      (val, oldVal) => {
        if (containerRef.value != undefined)
          containerHeight.value = containerRef.value?.clientWidth / val.width * val.height
      },
      {
        immediate: true
      }
  )
})
</script>

<style scoped>

</style>
