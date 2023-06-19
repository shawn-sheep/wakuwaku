<template>
  <div class="search-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">搜索结果</span>
    </div>
    <post-player-column-infinity v-if="show"
      :get-post-list="onGetImageList"
      :current-i="{tags: tags, per_page: 6, quality: 'sample', offset: 0}"
    ></post-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import store from "@/store";
import PostPlayerColumnInfinity from "@/components/postPlayerColumnInfinity.vue";
import {getPostPreviews, postPreview} from "@/assets/js/api";
import {ref, onMounted, defineProps, computed} from "vue";
import { useRoute } from "vue-router";

// 问号传参
const props = defineProps({
  tags: {
    type: String,
    required: true
  }
})

const show = ref(true);

const tags = ref(useRoute().query.tags)

// 监听路由变化
import { useRouter } from "vue-router";
const router = useRouter();
router.afterEach((to, from) => {
  tags.value = to.query.tags
  show.value = false
  setTimeout(() => {
    show.value = true
  }, 0)
})

const onGetImageList  = async (i : any) => {
  // return { newInfo: i, newImageList : store.state.recommend}
  console.log("onGetImageList", i)
  let res = await getPostPreviews(i)
  i.offset += i.per_page
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
