<template>
  <div>
    <div ref="containerRef" class="waterfall-div">
      <div
          v-for="i in info.columnCount"
          :key="i"
          class="waterfall-column"
          :style="{
            width: info.columnWidth + 'px'
          }"
          ref="columnsRef"
      >
        <waku-image
            v-for="item in info.imageListColumn[i-1]"
            :key="item"
            :img="item"
            fix-types="width"
            :size="info.columnWidth - 10"
        ></waku-image>
      </div>
    </div>
    <div class="more" ref="moreRef">
    </div>
  </div>
</template>

<script setup lang="ts">
import {reactive, withDefaults, defineProps, onMounted, ref, watch, onUnmounted} from "vue";
import {image, sleep} from "@/assets/js/api";
import WakuImage from "@/components/WakuImage.vue";

const props = withDefaults(defineProps<{
  columnMinWidth: number,
  getImageList: (info : any) => {newInfo : any, newImageList : image[]}
}>(), {
  columnMinWidth: 300,
  getImageList: (i : any) => { return {newInfo : i, newImageList : []} }
})

const info = reactive<{
  columnCount: number,
  columnWidth: number,
  imageList: image[],
  imageListColumn: Array<image>[],
  updating: boolean,
  currentI: any
}>({
  columnCount: 1,
  columnWidth: 0,
  imageList: [],
  imageListColumn: [[],[],[],[],[],[]],
  updating: false,
  currentI: {}
})

const containerRef = ref<Element>()
const moreRef = ref<Element>()
const columnsRef = ref<Element[]>([])

let intervalHook : number

onMounted(() => {
  intervalHook = setInterval(init, 300)
  const observer = new IntersectionObserver(([{ isIntersecting }]) => {
    if (isIntersecting) {
      if (!info.updating) {
        console.log('updating')
        info.updating = true
        more().then(() => {
          info.updating = false
        })
        console.log('async ok')
      }
    }
  }, {
    threshold: 0.5
  })
  observer.observe(moreRef.value) //观察指令绑定的dom
})

onUnmounted(() => {
  clearInterval(intervalHook)
})

watch(
    () => info.columnCount,
    async (val, preVal) => {
      while (info.updating);
      info.updating = true
      for (let i = 0; i < 6; ++i)
        info.imageListColumn[i].length = 0
      for (let i in info.imageList) {
        await insert(info.imageList[i])
      }
      info.updating = false
    },
    {}
)

const init = () => {
  info.columnCount = Math.floor(containerRef.value?.clientWidth / props.columnMinWidth);
  if (info.columnCount < 1) info.columnCount = 1
  if (info.columnCount > 6) info.columnCount = 6
  info.columnWidth = containerRef.value?.clientWidth / info.columnCount
}

const insert = async (img : image) => {
  info.imageList.push(img)
  let minHeight = 999999
  let c
  for (let column in columnsRef.value) {
    console.log()
    if (minHeight > columnsRef.value[column].clientHeight) {
      minHeight = columnsRef.value[column].clientHeight
      c = column
    }
  }
  console.log(c)
  info.imageListColumn[Number(c)].push(img)
  // sleep(1000)
}

const more = async () => {
  const {newInfo, newImageList} = props.getImageList(info.currentI)
  for (let item in newImageList) {
    await insert(newImageList[item])
  }
  info.currentI = newInfo
}
</script>

<style scoped>
.waterfall-div {
  display: flex;
}
.waterfall-column {
  box-sizing: border-box;
  padding: 5px;
  height: fit-content;
}
.more {
  height: 50px;
}
</style>
