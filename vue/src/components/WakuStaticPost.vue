<template>
  <div ref="containerRef" class="static-post-div" :style="{width: props.width === undefined ? '100%': props.width + 'px', height: isLoaded ? undefined : containerHeight + 'px' }">
    <transition name="fade" appear>
      <div style="width: 100%;position: absolute;background-color: #FFFFFF" v-if="(!isLoaded)" :style="{ height: containerHeight + 'px'}">
        <div style="position: absolute;top:50%;left: 50%;transform: translate(-50%, -50%)">
          <div class="spinner-5"></div>
        </div>
      </div>
    </transition>
    <img
        v-if="!isVideo"
        :src="props.img === undefined ? '': props.img.sample_url"
        @load="onLoaded"
    >
    <video
        v-if="isVideo"
        :style="{visibility: isLoaded ? 'visible' : 'hidden'}"
        :src="props.img === undefined ? '': props.img.sample_url"
        @loadedmetadata="onLoaded"
        controls
    ></video>
  </div>
</template>

<script setup lang="ts">
import {image} from "@/assets/js/api";
import {computed, onMounted, onUnmounted, ref, watch} from "vue";

// eslint-disable-next-line no-undef
const props = defineProps<{
  img : image
  width ?: number
  height ?: number
}>()

const containerRef = ref<Element>()
const containerHeight = ref<number>(0)
const isLoaded = ref<boolean>(false)

let intervalHook : number

onMounted(() => {
  console.log('mounted')
  calcContainerHeight()
  intervalHook = setInterval(calcContainerHeight, 300)
  watch(
      () => props.img,
      (val, oldVal) => {
        if(val.sample_url != oldVal?.sample_url) {
          isLoaded.value = false
          calcContainerHeight()
        }
      },
      {
        immediate : true
      }
  )
})

onUnmounted(() => {
  console.log('unmounted')
  clearInterval(intervalHook)
})

const calcContainerHeight = () => {
  // console.log('calc')
  if (isLoaded.value) return
  if (props.height != undefined) {
    containerHeight.value = props.height;
    return;
  }
  let calcWidth = 0
  if (props.width != undefined) calcWidth = props.width
  else if (containerRef.value != undefined) calcWidth = containerRef.value?.clientWidth
  containerHeight.value = calcWidth / props.img.width * props.img.height
  // console.log(containerRef.value?.clientWidth)
}

const isImage = computed(() => {
  if (props.img === undefined) return false;
  return props.img.sample_url.match(/\.(jpg|jpeg|png|gif)$/i)
})

const isVideo = computed(() => {
  if (props.img === undefined) return false;
  return props.img.sample_url.match(/\.(mp4|webm|ogg)$/i)
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
  background-color: rgba(0, 0, 0, 0.02);
}
img,video {
  max-width: 100%;
}
</style>