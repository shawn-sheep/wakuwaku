<template>
  <div>
    <waku-static-post :img="info.img"></waku-static-post>
  </div>
</template>

<script setup lang="ts">
import {defineProps, onMounted, reactive, ref, watch} from 'vue'
import {getImageByID, image} from "@/assets/js/api";
import WakuStaticPost from "@/components/WakuStaticPost.vue";
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
