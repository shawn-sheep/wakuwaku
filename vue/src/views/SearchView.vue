<template>
  <div class="search-div">
    <!-- <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">搜索结果</span>
    </div> -->
    <!-- <div class="order-conditions">
      <waku-button style="width: 100px;text-align: center" :enable="true"
        :font-color='"var(--wakuwaku-header-font-color)"'
        :color='"var(--wakuwaku-header-background-color)"'
      >最新发布</waku-button>
    </div> -->
    <WakuButtonGroup :options="['最新发布', '最旧发布', '分数最高']"
      :type="'single'" :selected-options="[order ? orderParams.indexOf(order as string) : 0]"
      @update:selected-options="onUpdateOrderOptions"
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
import { useRoute } from "vue-router";

import WakuButtonGroup from "@/components/WakuButtonGroup.vue";

const show = ref(true);

const tags = ref(useRoute().query.tags)
const order = ref(useRoute().query.order ? useRoute().query.order : "new")

// 监听路由变化
import { useRouter } from "vue-router";
const router = useRouter();
router.afterEach((to, _from) => {
  tags.value = to.query.tags
  show.value = false
  setTimeout(() => {
    show.value = true
  }, 0)
})

const orderParams = ["new", "old", "score"]

const onUpdateOrderOptions = (i : number[]) => {
  console.log("onUpdateOrderOptions", i)
  order.value = orderParams[i[0]]
  router.push({query: {tags: tags.value, order: order.value}})
}

const onGetImageList  = async (i : any) => {
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
