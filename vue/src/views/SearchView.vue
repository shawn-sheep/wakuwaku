<template>
  <div class="search-div">
    <div class="search-options">
    <WakuButtonGroup :options="['最新发布', '最旧发布', '分数最高']"
      :type="'single'" :selected-options="orderOptions"
      @update:selected-options="onUpdateOrderOptions"
    ></WakuButtonGroup>
    <WakuButtonGroup :options="['G', 'S', 'Q', 'E']" class="rating-options"
      :type="'multiple'" :selected-options="ratingsOptions"
      @update:selected-options="onUpdateRatingOptions"
    ></WakuButtonGroup>
    </div>
    <post-player-column-infinity v-if="show"
      :get-post-list="onGetImageList"
      :current-i="{per_page: 6, quality: 'sample', offset: 0, tags: tags, order: order, ratings: ratings}"
    ></post-player-column-infinity>
  </div>
</template>

<script setup lang="ts">
import PostPlayerColumnInfinity from "@/components/postPlayerColumnInfinity.vue";
import { getPostPreviews, goto } from "@/assets/js/api";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import WakuButtonGroup from "@/components/WakuButtonGroup.vue";

const show = ref(true);

const route = useRoute()
const tags = ref(route.query.tags)
const order = ref(route.query.order ? route.query.order : "new")
const ratings = ref(route.query.ratings ? route.query.ratings as string : "g")

const orderOptions = computed(() => {
  return [orderParams.indexOf(order.value as string)]
})
const ratingsOptions = computed(() => {
  if (ratings.value === '') return []
  return ratings.value.split(" ").map((i : string) => ["g", "s", "q", "e"].indexOf(i))
})

// 监听路由变化
import { onBeforeRouteUpdate } from "vue-router";
import { computed } from "vue";
onBeforeRouteUpdate((to, from, next) => {
  console.log("onBeforeRouteUpdate", to.query.tags)
  tags.value = to.query.tags
  order.value = to.query.order ? to.query.order : "new"
  ratings.value = to.query.ratings !== undefined ? to.query.ratings as string : "g"
  show.value = false
  setTimeout(() => {
    show.value = true
  }, 0)
  next()
})

const orderParams = ["new", "old", "score"]

const onUpdateOrderOptions = (i : number[]) => {
  console.log("onUpdateOrderOptions", i)
  goto({query: {tags: tags.value, order: orderParams[i[0]], ratings: ratings.value}})
}

const onUpdateRatingOptions = (i : number[]) => {
  console.log("onUpdateRatingOptions", i)
  goto({query: {tags: tags.value, order: order.value, ratings: i.map((i : number) => ["g", "s", "q", "e"][i]).join(" ")}})
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

.search-options {
  /* between */
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-bottom: 20px;
}

:deep .rating-options.waku-button-group button {
  margin: 0 5px;
  padding: 10px 10px;
  font-weight: 600;
  font-size: 16px;
}
</style>
