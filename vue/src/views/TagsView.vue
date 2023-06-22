<template>
  <!-- <div class="tags-div">
    <div style="text-align: left">
      <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">排行榜</span>
    </div>
  </div> -->
  <div class="tags-div">
    <div class="tag-div" v-for="item in type_names" :key="item.name">
      <div class="tag-type-div" style="text-align: left" v-if="tags_by_type[item.type]">
        <span style="font-size: 18px; font-weight: 800; color: var(--wakuwaku-font-color); padding-left: 20px;padding-top: 5px">{{ item.name }}</span>
      </div>
      <div class="tags">
        <waku-tag v-for="tag in tags_by_type[item.type]" :key="tag.tag_id" :tag="tag"></waku-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {tag, getTags} from "@/assets/js/api";
import {ref, onMounted} from "vue";
import WakuTag from "@/components/WakuTag.vue";

const type_names = [
  { type: 1, name: '画师' },
  { type: 3, name: '作品' },
  { type: 4, name: '角色' },
  { type: 0, name: '标签' },
  { type: 5, name: '信息' }
]

const tags_by_type = ref<Record<number, tag[]>>({})

onMounted(async () => {
  for (const tag of await getTags(50)) {
    if (tags_by_type.value[tag.type] === undefined) {
      tags_by_type.value[tag.type] = []
    }
    tags_by_type.value[tag.type].push(tag)
  }
})
</script>

<style scoped>
.tags-div {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}

.tag-type-div {
  margin: 10px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: center;
  /* padding: 0 10px; */
}
</style>
