<template>
  <div>
    <transition name="pull-down">
      <div class="user-bar-div" v-if="props.expand">
        <div style="height: 70px;background-color: var(--wakuwaku-color)"></div>
        <div class="user-bar-item" style="position: relative;height: 20px">
          <waku-avatar style="position: absolute; bottom: 0" :size="80" :src="store.state.user.avatar_url"></waku-avatar>
        </div>
        <div class="user-bar-item" style="font-size: 18px;font-weight: 600;">{{ store.state.user.username }}</div>
        <div class="user-bar-item" style="font-size: 12px">{{ store.state.user.email }}</div>
        <div style="height: 20px"></div>
        <div class="user-bar-item2" @click="goto(`/user/${store.state.user.account_id}`, true)">个人主页</div>
        <div class="user-bar-item2" @click="goto('/userinfo', true)">信息修改</div>
        <div class="user-bar-item2" @click="goto('/upload', true)">上传图片</div>
        <div style="height: 60px"></div>
        <div class="user-bar-item2" @click="logout()">登出</div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import {defineProps} from 'vue'
import WakuAvatar from "@/components/WakuAvatar.vue";
import store from "@/store";
import {goto,logout} from "@/assets/js/api";

const props = defineProps<{
  expand : boolean
}>();

// eslint-disable-next-line no-undef
// const emits = defineEmits(['fold'])
//
// const onClickOutside = () => {
//   emits('fold')
// }
</script>

<style scoped>
.user-bar-div {
  position: absolute;
  width: 220px;
  height: var(--wakuwaku-user-bar-height);
  background-color: #FFFFFF;
  left: -150px;
  top: 60px;
  border-radius: 10px;
  transition: height 0.2s;
  border: var(--wakuwaku-color-dark) 1px solid;
  overflow: hidden;
  text-align: left;
  /*color: var(--wakuwaku-font-color);*/
}
.user-bar-item {
  margin: 3px 0;
  padding-left: 30px;
}
.user-bar-item2 {
  padding: 10px 0 10px 30px;
  transition: background-color 0.1s;
}
.user-bar-item2:hover {
  background-color: var(--wakuwaku-color-light);
}
</style>
