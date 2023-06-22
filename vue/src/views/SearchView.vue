<template>
  <div class="search-div">
    <WakuButtonGroup :options="['最新发布', '最旧发布', '分数最高']"
      :type="'single'" :selected-options="orderOptions"
      @update:selected-options="onUpdateOrderOptions"
      style="margin-bottom: 20px;"
    ></WakuButtonGroup>
    <post-player-column-infinity v-if="show"
      :get-post-list="onGetImageList"
      :current-i="{per_page: 6, quality: 'sample', offset: 0, tags: tags, order: order}"
    ></post-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import PostPlayerColumnInfinity from "@/components/postPlayerColumnInfinity.vue";
import { getPostPreviews } from "@/assets/js/api";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import WakuButtonGroup from "@/components/WakuButtonGroup.vue";

const show = ref(true);

const tags = ref(useRoute().query.tags)
const order = ref(useRoute().query.order ? useRoute().query.order : "new")

const orderOptions = computed(() => {
  return [orderParams.indexOf(order.value as string)]
})

// 监听路由变化
import { onBeforeRouteUpdate } from "vue-router";
import { computed } from "vue";
onBeforeRouteUpdate((to, from, next) => {
  console.log("onBeforeRouteUpdate", to.query.tags)
  tags.value = to.query.tags
  order.value = to.query.order ? to.query.order : "new"
  show.value = false
  setTimeout(() => {
    show.value = true
  }, 0)
  next()
})
const router = useRouter();
// router.afterEach((to) => {
//   tags.value = to.query.tags
//   show.value = false
//   setTimeout(() => {
//     show.value = true
//   }, 0)
// })

const orderParams = ["new", "old", "score"]

const onUpdateOrderOptions = (i : number[]) => {
  console.log("onUpdateOrderOptions", i)
  router.push({query: {tags: tags.value, order: orderParams[i[0]]}})
}

const onGetImageList  = async (i : { offset : number, per_page : number } ) => {
  // return { newInfo: i, newImageList : store.state.recommend}
  console.log("onGetImageList", i)
  let res = await getPostPreviews(i)
  i.offset += i.per_page
  return { newInfo: i, newPostList : res}
}
</script>

<style scoped>
.search-div {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}

select:focus {
  outline: none;
}
</style>
