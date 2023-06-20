<template>
  <div>
    <div style="display: flex; width: 100%; height: 100%">
      <div ref="scrollRef" class="scroll-wrap">
        <div
            ref="contentRef"
            class="content"
            :style="{
              left: - info.leftPercentage * info.contentWidth / 100 + 'px',
              top: - info.topPercentage * info.contentHeight / 100 + 'px',
              width: props.scrollDirection === 'row' ? 'fit-content' : '100%'
            }"
            @wheel="onWheel"
        >
          <slot name="default" ></slot>
        </div>
      </div>
      <div ref="barVerticalRef" class="scrollbar vertical" v-if="props.scrollDirection === 'column'">
        <div
          class="scrollbar-thumb"
          :style="{
            height: info.heightPercentage + '%',
            top: info.topPercentage + '%'
          }"
          @mousedown="onMouseDown"
        ></div>
      </div>
    </div>
    <div ref="barHorizontalRef" class="scrollbar horizontal" v-if="props.scrollDirection === 'row'">
      <div
          class="scrollbar-thumb"
          :style="{
            width: info.widthPercentage + '%',
            left: info.leftPercentage + '%'
          }"
          @mousedown="onMouseDown"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch } from "vue";
import {onMounted, onUnmounted, reactive, ref} from "vue";

// eslint-disable-next-line no-undef
const props = withDefaults(defineProps<{
    scrollDirection?: string
  }>(),{
    scrollDirection: 'row'
  }
)

const contentRef = ref<HTMLDivElement>()
const scrollRef = ref<HTMLDivElement>()
const barVerticalRef = ref<HTMLDivElement>()
const barHorizontalRef = ref<HTMLDivElement>()

const info = reactive({
  barWidth: 0,
  barHeight: 0,
  thumbWidth: 0,
  thumbHeight: 0,
  contentWidth: 0,
  contentHeight: 0,
  widthPercentage: 0,
  heightPercentage: 0,
  leftPercentage: 0,
  topPercentage: 0,
  isMove: false,
  moveClientX: 0,
  moveClientY: 0,
})

let intervalHook : number

onMounted(() => {
  intervalHook = setInterval(updateScroll, 300)
})

onUnmounted(() => {
  clearInterval(intervalHook)
})

const updateScroll = () => {
  if (props.scrollDirection === 'row') {
    info.barWidth = barHorizontalRef.value.clientWidth
    info.contentWidth = contentRef.value.clientWidth
    if (scrollRef.value.clientWidth > contentRef.value.clientWidth)
      info.widthPercentage = 100
    else
      info.widthPercentage = scrollRef.value.clientWidth / contentRef.value.clientWidth * 100;
    info.thumbWidth = info.barWidth * info.widthPercentage / 100;
    if (info.leftPercentage + info.widthPercentage > 100)
      info.leftPercentage = 100 - info.widthPercentage
    if (info.leftPercentage < 0)
      info.leftPercentage = 0
  } else if (props.scrollDirection === 'column') {
    info.barHeight = barVerticalRef.value.clientHeight
    // 修正高度变化时的滚动条位置
    if (info.contentHeight != contentRef.value.clientHeight) {
      info.topPercentage = info.topPercentage * info.contentHeight / contentRef.value.clientHeight
    }
    info.contentHeight = contentRef.value.clientHeight
    if (scrollRef.value.clientHeight > contentRef.value.clientHeight)
      info.heightPercentage = 100
    else
      info.heightPercentage = scrollRef.value.clientHeight / contentRef.value.clientHeight * 100;
    info.thumbHeight = info.barHeight * info.heightPercentage / 100;
    if (info.topPercentage + info.heightPercentage > 100)
      info.topPercentage = 100 - info.heightPercentage
    if (info.topPercentage < 0)
      info.topPercentage = 0
  }
}

const onMouseDown = (e : any) => {
  info.isMove = true
  if (props.scrollDirection === 'row')
    info.moveClientX = e.clientX
  else info.moveClientY = e.clientY
  document.onmousemove = onMouseMove
  document.onmouseup = onMouseUp
}

const onMouseMove = (e : any) => {
  if (info.isMove) {
    if(props.scrollDirection === 'row') {
      info.leftPercentage += (e.clientX - info.moveClientX) / info.barWidth * 100;
      if (info.leftPercentage + info.widthPercentage > 100)
        info.leftPercentage = 100 - info.widthPercentage
      if (info.leftPercentage < 0)
        info.leftPercentage = 0
      info.moveClientX = e.clientX
    } else {
      info.topPercentage += (e.clientY - info.moveClientY) / info.barHeight * 100;
      if (info.topPercentage + info.heightPercentage > 100)
        info.topPercentage = 100 - info.heightPercentage
      if (info.topPercentage < 0)
        info.topPercentage = 0
      info.moveClientY = e.clientY
    }
  }
}

const onMouseUp = (e : any) => {
  if (info.isMove) {
    info.isMove = false
  }
}

const onWheel = (e : any) => {
  if(props.scrollDirection === 'column') {
    info.topPercentage += e.deltaY / info.contentHeight * 75
    if (info.topPercentage + info.heightPercentage > 100)
      info.topPercentage = 100 - info.heightPercentage
    if (info.topPercentage < 0)
      info.topPercentage = 0
    info.moveClientY = e.clientY
  }
}
</script>

<style scoped>
/*::-webkit-scrollbar {*/
/*  width: 5px;*/
/*  height: 50%;*/
/*  border-radius: 999px;*/
/*  background-color: var(--wakuwaku-background-color);*/
/*}*/
/*::-webkit-scrollbar-thumb {*/
/*  border-radius: 999px;*/
/*  background-color: var(--wakuwaku-background-color);*/
/*}*/
.scroll-wrap {
  overflow: hidden;
  width: 100%;
}
.content {
  position: relative;
  transition: top 0.1s, left 0.1s;
}
.scrollbar {
  background-color: var(--wakuwaku-scrollbar-color);
  border-radius: 999px;
}
.horizontal {
  width: 40%;
  min-width: 200px;
  margin-top: 5px;
  margin-left: auto;
  margin-right: auto;
  height: 5px;
}
.vertical {
  height: 40%;
  min-height: 200px;
  width: 5px;
  margin-top: auto;
  margin-bottom: auto;
  margin-right: 5px;
}
.scrollbar-thumb {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: var(--wakuwaku-scrollbar-thumb-color);
  border-radius: 999px;
  transition: top 0.1s, left 0.1s;
}
</style>
