<template>
  <div ref="containerRef" class="static-post-div" :style="{width: props.width === undefined ? '100%': props.width + 'px', height: containerHeight + 'px'}">
    <transition name="fade" appear>
      <div style="width: 100%;height: 100%;position: absolute;background-color: #FFFFFF" v-if="(!isLoaded) && isImage">
        <div style="position: absolute;top:50%;left: 50%;transform: translate(-50%, -50%)">
          <div class="spinner-5"></div>
        </div>
      </div>
    </transition>
    <img
        v-if="isImage"
        :src="img === undefined ? '': img.src"
        @load="onLoaded"
    >
    <video
        v-if="isVideo"
        :src="img === undefined ? '': img.src"
        @load="onLoaded"
        controls
    ></video>
  </div>
</template>

<script setup lang="ts">
import {image} from "@/assets/js/api";
import {computed, onMounted, onUnmounted, ref, watch} from "vue";
import store from "@/store";

// eslint-disable-next-line no-undef
const props = defineProps<{
  img : image,
  width: number,
  height: number
}>()

const img = ref<image>()
const containerRef = ref<Element>()
const containerHeight = ref<number>(0)
const isLoaded = ref<boolean>(false)

watch(
    () => props.img,
    (val, oldVal) => {
      isLoaded.value = false
      img.value = val
    },
    {
      immediate : true
    }
)

let intervalHook : number

onMounted(() => {
  intervalHook = setInterval(calcContainerHeight, 300)
})

onUnmounted(() => {
  clearInterval(intervalHook)
})

const calcContainerHeight = () => {
  if (props.height != undefined) {
    containerHeight.value = props.height;
    return;
  }
  let calcWidth = 0
  if (props.width != undefined) calcWidth = props.width
  else if (containerRef.value != undefined) calcWidth = containerRef.value?.clientWidth
  containerHeight.value = calcWidth / props.img.width * props.img.height
  console.log(containerHeight.value)
}

const isImage = computed(() => {
  if (img.value === undefined) return false;
  return img.value.src.match(/\.(jpg|jpeg|png|gif)$/i)
})

const isVideo = computed(() => {
  if (img.value === undefined) return false;
  return img.value.src.match(/\.(mp4|webm|ogg)$/i)
})

const onLoaded = () => {
  isLoaded.value = true
}
</script>

<style scoped>
.static-post-div {
  border-radius: 20px;
  overflow: hidden;
  width: 100%;
  position: relative;
  margin: auto;
}
img,video {
  width: 100%;
  height: 100%;
}
</style>
