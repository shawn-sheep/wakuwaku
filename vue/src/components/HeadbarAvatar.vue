<template>
  <div style="position: relative">
    <div class="headbar-avatar-div" @click="isExpand = !isExpand">
      <!--    <div style="font-size: 18px; font-weight: 600">{{ store.state.user.username }}</div>-->
      <WakuAvatar :src="store.state.user.avatar_url" :size="38" style="padding-left: 10px;padding-right: 5px"></WakuAvatar>
      <div class="pull-down">
        <svg style="height: 10px;width: 10px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="CurrentColor" fill="CurrentColor"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
      </div>
    </div>
    <user-bar :expand="isExpand"></user-bar>
  </div>
</template>

<script setup lang="ts">
import WakuAvatar from "@/components/WakuAvatar.vue";
import store from "@/store";
import {ref} from "vue";
import UserBar from "@/components/UserBar.vue";

const isExpand = ref<boolean>(false)
</script>

<style scoped>
.headbar-avatar-div {
  display: flex;
  flex-direction: row;
  cursor: pointer;
}
.pull-down {
  margin: auto 20px auto 0;
  transition: color 0.1s;
}
.headbar-avatar-div:hover .pull-down {
  color: var(--wakuwaku-header-hover-color);
}
</style>
