<template>
  <div class="home-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">排行榜</span>
    </div>
    <ImagePlayerRow :image-list="store.state.recommend"></ImagePlayerRow>
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">最新更新</span>
    </div>
    <ImagePlayerRow :image-list="store.state.recommend"></ImagePlayerRow>
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

const onGetImageList  = (i : any) => {
  return { newInfo: i, newImageList : store.state.recommend}
}
</script>

<style scoped>
.home-div {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}
</style>
