<template>
  <div class="comment-div">
    <waku-avatar :src="props.comment.avatar_url ? props.comment.avatar_url : require('@/assets/img/user_avatar.jpg')" :size="40"></waku-avatar>
    <div style="width: 100%">
      <div class="username-div">{{ props.comment.username }}</div>
      <div class="content-div">{{ props.comment.content }}</div>
      <waku-link style="width: 50px;height: 20px;font-size: 12px" @click="emits('reply',props.comment)">回复</waku-link>
      <waku-comment v-for="item in props.comment.replies" :key="item.comment_id" :comment="item" @reply="fn"></waku-comment>
    </div>
  </div>
</template>

<script setup lang="ts">
import {comment} from "@/assets/js/api";
import {defineProps, withDefaults} from 'vue'
import WakuAvatar from "@/components/WakuAvatar.vue";
import WakuLink from "@/components/WakuLink.vue";

const props = withDefaults(
    defineProps<{
      comment : comment
    }>(), {
      comment : () => new comment()
    }
)

// eslint-disable-next-line no-undef
const emits = defineEmits(['reply'])

const fn = (comment : comment) => {
  emits('reply', comment)
}
</script>

<style scoped>
.comment-div {
  width: 100%;
  display: flex;
  flex-direction: row;
  margin: 20px 0 0 0;
  gap: 20px;
  height: auto;
}
.username-div {
  font-weight: 800;
  font-size: 16px;
  margin: 0 0 10px 0;
}
.content-div {
  margin: 10px 0;
  white-space: pre-wrap;
  font-size: 14px;
}
</style>
