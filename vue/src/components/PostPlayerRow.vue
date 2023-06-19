<template>
  <div style="width: 100%;margin-bottom: 10px">
    <waku-scroller>
      <div class="image-display-div">
        <waku-post
            v-for="item in props.postList"
            v-bind:key="item"
            :post="item"
            :size="200"
            fix-types="height"
        ></waku-post>
      </div>
    </waku-scroller>
  </div>
</template>

<script setup lang="ts">
import WakuPost from "@/components/WakuPost.vue";
import WakuScroller from "@/components/WakuScroller";
import {postPreview} from "@/assets/js/api";

// eslint-disable-next-line no-undef
const props = defineProps<{
  postList: postPreview[]
}>()
</script>

<style scoped>
.image-display-div {
  /*height: 200px;*/
  display: flex;
  flex-direction: row;
  width: fit-content;
  padding-top: 10px;
}
</style>
