<template>
  <div style="width: 100%;margin-bottom: 10px">
    <waku-scroller>
      <div class="image-display-div">
        <waku-image
            v-for="item in props.imageList"
            v-bind:key="item"
            :img="item"
            :size="200"
            fix-types="height"
        ></waku-image>
      </div>
    </waku-scroller>
  </div>
</template>

<script setup lang="ts">
import WakuImage from "@/components/WakuImage.vue";
import WakuScroller from "@/components/WakuScroller";

// eslint-disable-next-line no-undef
const props = defineProps({
  imageList : Array
})
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
