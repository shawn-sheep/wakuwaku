<template>
  <div class="home-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">排行榜</span>
    </div>
    <ImagePlayerRow :image-list="rank_images"></ImagePlayerRow>
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">最新更新</span>
    </div>
    <ImagePlayerRow :image-list="recent_images"></ImagePlayerRow>
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">每日推荐</span>
    </div>
    <image-player-column-infinity
        :get-image-list="onGetImageList"
    ></image-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import ImagePlayerRow from "@/components/ImagePlayerRow";
import store from "@/store";
import ImagePlayerColumnInfinity from "@/components/ImagePlayerColumnInfinity";
import {image, getImages} from "@/assets/js/api";
import {ref, onMounted} from "vue";

let rank_images = ref<image[]>([])
let recent_images = ref<image[]>([])

onMounted(async () => {
  rank_images.value = await getImages({order: "rank"})
  recent_images.value = await getImages({order: "new"})
})

const onGetImageList  = async (i : any) => {
  // return { newInfo: i, newImageList : store.state.recommend}
  console.log("onGetImageList", i)
  let res = await getImages(i)
  i.before_id = res[res.length - 1].id
  return { newInfo: i, newImageList : res}
}
</script>

<style scoped>
.home-div {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}
</style>
