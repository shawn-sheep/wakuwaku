<template>
  <div>
    <waku-static-image :img="info.img"></waku-static-image>
  </div>
</template>

<script setup lang="ts">
import {defineProps, onMounted, reactive, ref, watch} from 'vue'
import {getImageByID, image} from "@/assets/js/api";
import WakuStaticImage from "@/components/WakuStaticImage.vue";
const props = defineProps<{
  id : string
}>()

const info = reactive<{
  img : image
}>({
  img : new image()
})

onMounted(() => {
  watch(
      () => props.id,
      (val, oldVal) => {
        updateImage(val)
      },
      {
        immediate: true
      }
  )
})

const updateImage = (id : string) => {
  getImageByID(id).then((res) => {
    info.img = res
    console.log(info.img)
  })
}
</script>

<style scoped>

</style>
