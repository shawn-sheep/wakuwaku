<template>
  <div class="search-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">搜索结果</span>
    </div>
    <post-player-column-infinity
      :get-post-list="onGetImageList"
      :current-i="{tags: useRoute().query.tags, per_page: 6, quality: 'sample'}"
    ></post-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import store from "@/store";
import PostPlayerColumnInfinity from "@/components/postPlayerColumnInfinity.vue";
import {getPostPreviews, postPreview} from "@/assets/js/api";
import {ref, onMounted, defineProps, watch} from "vue";
import { useRoute } from "vue-router";
import { getCurrentInstance } from "vue";

// 问号传参
const props = defineProps({
  tags: {
    type: String,
    required: true
  }
})

let tags = useRoute().query.tags
console.log("tags", tags)

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
