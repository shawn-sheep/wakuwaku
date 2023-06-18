<template>
  <waku-link class="tag">
    <div>
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="CurrentColor" fill="CurrentColor"><path d="M10.773 21.585l-1.368 1.415-10.405-10.429v-8.571h2v7.719l9.773 9.866zm1.999-20.585h-9.772v9.772l12.074 12.228 9.926-9.85-12.228-12.15zm-4.772 7c-1.105 0-2-.895-2-2s.895-2 2-2 2 .895 2 2-.895 2-2 2z"/></svg>
    </div>
    <span>{{ props.tag.name + '[' + countToString() + ']' }}</span>
  </waku-link>
</template>

<script setup lang="ts">
import WakuLink from "@/components/WakuLink";
import {tag} from "@/assets/js/api";
import {defineProps} from 'vue'

const props = defineProps<{
  tag : tag
}>()

const countToString = () => {
  if(props.tag.count > 1000000) return Math.floor(props.tag.count/1000000) + 'M'
  if(props.tag.count > 1000) return Math.floor(props.tag.count/1000) + 'K'
  else return props.tag.count
}

</script>

<style scoped>
.tag {
  height: 18px;
  display: inline-block;
  margin-right: 10px;
  font-size: 14px;
}
.tag div {
  display: inline-block;
  vertical-align: middle;
  width: 20px;
  height: 16px;
}
svg {
  width: 16px;
  height: 16px;
}
</style>
