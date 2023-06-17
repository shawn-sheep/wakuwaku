<template>
  <div class="image-div" @mouseenter="onMouseEnter" @mouseleave="onMouseLeave" @click="onClick" :class="{'loaded': isLoaded}">
    <div class="info-div" :style="{opacity: ishover? 1 : 0}">
      <div class="info-center-div">
        {{ props.img.description }}
      </div>
    </div>
    <transition name="fade" appear>
      <div style="width: 100%;height: 100%;position: absolute;background-color: #FFFFFF" v-if="!isLoaded">
        <div style="position: absolute;top:50%;left: 50%;transform: translate(-50%, -50%)">
          <div class="spinner-5"></div>
        </div>
      </div>
    </transition>
    <div
        :style="{
           width: props.fixTypes === 'width' ? props.size + 'px' : 'auto',
           height: props.fixTypes === 'height' ? props.size + 'px' : 'auto'
         }"
        style="transition: height 1s, width 1s"
    >
      <img
          @load = "onLoad"
          v-lazyload="props.img.src"
          :style="{
             width: props.fixTypes === 'width' ? '100%' : (isLoaded ? '' : props.size + 'px'),
             height: props.fixTypes === 'height' ? '100%' : (isLoaded ? '' : props.size + 'px'),
          }"
      >
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {showImage} from "@/assets/js/api";

// eslint-disable-next-line no-undef
const props = defineProps({
  img: Object,
  size: Number,
  fixTypes: String
})

const ishover = ref(false)

const isLoaded = ref(false)

const onMouseEnter = () => {
  ishover.value = true
}

const onMouseLeave = () => {
  ishover.value = false
}

const onClick = () => {
  showImage(props.img)
}

const onLoad = () => {
  isLoaded.value = true
}
</script>

<style scoped>
.image-div {
  position: relative;
  margin: 3px;
  border-radius: 15px;
  overflow: hidden;
}
.info-div {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgb(0,0,0, 0.5);
  transition: opacity 0.1s;
}
.info-center-div {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  max-width: 80%;
  color: #FFFFFF;
  font-size: 14px;
}
img[src=''],
img:not([src]) {
  opacity: 0;
  min-height: 10px;
  min-width: 10px;
}
.spinner-5 {
  width: 50px;
  --b: 8px; /* the border thickness */
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--wakuwaku-header-font-color);
  -webkit-mask:
      repeating-conic-gradient(#0000 0deg,#000 1deg 70deg,#0000 71deg 90deg),
      radial-gradient(farthest-side,#0000 calc(100% - var(--b) - 1px),#000 calc(100% - var(--b)));
  -webkit-mask-composite: destination-in;
  mask-composite: intersect;
  animation: s5 1s infinite;
}
@keyframes s5 {to{transform: rotate(.5turn)}}

.loaded {
  animation: shrink 0.5s, fade 0.5s;
}
</style>
