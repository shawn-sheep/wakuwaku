<template>
  <div class="search-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">搜索结果</span>
    </div>
    <image-player-column-infinity
        :get-image-list="onGetImageList"
    ></image-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import store from "@/store";
import ImagePlayerColumnInfinity from "@/components/ImagePlayerColumnInfinity.vue";
import {image, getImages} from "@/assets/js/api";
import {ref, onMounted, defineProps} from "vue";
import { useRoute } from "vue-router";

// 问号传参
const props = defineProps({
  tags: {
    type: String,
    required: true
  }
})

onMounted(async () => {
  // 从路由中获取参数
  let tags = useRoute().query.tags
  console.log("tags", tags)
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
