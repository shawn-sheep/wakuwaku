<template>
  <div class="home-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">排行榜</span>
    </div>
    <post-player-row :post-list="rank_images"></post-player-row>
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">最新更新</span>
    </div>
    <post-player-row :post-list="recent_images"></post-player-row>
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">每日推荐</span>
    </div>
    <post-player-column-infinity
        :get-post-list="onGetImageList"
    ></post-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import PostPlayerRow from "@/components/PostPlayerRow.vue";
import PostPlayerColumnInfinity from "@/components/postPlayerColumnInfinity.vue";
import {getPostPreviews, postPreview} from "@/assets/js/api";
import {ref, onMounted} from "vue";

let rank_images = ref<postPreview[]>([])
let recent_images = ref<postPreview[]>([])

onMounted(async () => {
  rank_images.value = await getPostPreviews({order: "rank"})
  recent_images.value = await getPostPreviews({order: "new"})
})

const onGetImageList  = async (i : any) => {
  // return { newInfo: i, newImageList : store.state.recommend}
  console.log("onGetImageList", i)
  let res = await getPostPreviews(i)
  i.before_id = res[res.length - 1].post_id
  return { newInfo: i, newPostList : res}
}
</script>

<style scoped>
.home-div {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}
</style>
