<template>
  <div style="background-color: var(--wakuwaku-color-light);padding: 20px;">
    <div class="user-div">
      <div class="user-background"></div> <!--这里可以让用户自定义背景-->
      <div style="height: 50px;position: relative">
        <waku-avatar :size="150" :src="store.state.user.avatar_url" style="margin: auto;top: -100px;position: relative;">
        </waku-avatar>
        <div class="button-div" v-if="isSelf">
          <div class="button-item" title="修改个人信息">
            <div style="margin: auto">
              <svg style="width: 20px;height: 20px;margin:auto" fill="CurrentColor" stroke="CurrentColor" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m19 20.25c0-.402-.356-.75-.75-.75-2.561 0-11.939 0-14.5 0-.394 0-.75.348-.75.75s.356.75.75.75h14.5c.394 0 .75-.348.75-.75zm-12.023-7.083c-1.334 3.916-1.48 4.232-1.48 4.587 0 .527.46.749.749.749.352 0 .668-.137 4.574-1.493zm1.06-1.061 3.846 3.846 8.824-8.814c.195-.195.293-.451.293-.707 0-.255-.098-.511-.293-.706-.692-.691-1.742-1.741-2.435-2.432-.195-.195-.451-.293-.707-.293-.254 0-.51.098-.706.293z" fill-rule="nonzero"/></svg>
            </div>
          </div>
          <div class="button-item" title="上传图片">
            <div style="margin: auto">
              <svg style="width: 20px;height: 20px;margin:auto" fill="CurrentColor" stroke="CurrentColor" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M16 16h-3v5h-2v-5h-3l4-4 4 4zm3.479-5.908c-.212-3.951-3.473-7.092-7.479-7.092s-7.267 3.141-7.479 7.092c-2.57.463-4.521 2.706-4.521 5.408 0 3.037 2.463 5.5 5.5 5.5h3.5v-2h-3.5c-1.93 0-3.5-1.57-3.5-3.5 0-2.797 2.479-3.833 4.433-3.72-.167-4.218 2.208-6.78 5.567-6.78 3.453 0 5.891 2.797 5.567 6.78 1.745-.046 4.433.751 4.433 3.72 0 1.93-1.57 3.5-3.5 3.5h-3.5v2h3.5c3.037 0 5.5-2.463 5.5-5.5 0-2.702-1.951-4.945-4.521-5.408z"/></svg>
            </div>
          </div>
        </div>
      </div>
      <div style="font-weight: 600;font-size: 24px;margin: 10px 0"> {{ store.state.user.username }} </div>
      <div style="font-size: 12px;color: #AAAAAA"> {{ store.state.user.email}} </div>
      <div class="upload-or-like-selector">
        <div
            class="selector-item"
            @click="displayType = 'uploads'"
            :class="{'selected' : displayType === 'uploads'}"
        >
          我的上传
        </div>
        <div
            class="selector-item"
            @click="displayType = 'likes'"
            :class="{'selected' : displayType === 'likes'}"
        >
          我的收藏
        </div>
      </div>
      <div style="width: 100%">
        <post-player-column-infinity v-if="displayType === 'uploads'"></post-player-column-infinity>
        <post-player-column-infinity v-if="displayType === 'likes'"></post-player-column-infinity>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import WakuAvatar from "@/components/WakuAvatar";
import store from "@/store";
import {ref} from "vue";
import PostPlayerColumnInfinity from "@/components/postPlayerColumnInfinity.vue";

const displayType = ref<string>('uploads')
const isSelf = ref<boolean>(true)

</script>

<style scoped>
.user-div {
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
  background-color: #FFFFFF;
}
.user-background {
  height: 250px;
  background-color: var(--wakuwaku-color);
  transition: height 0.2s ease-in-out;
}
.user-background:hover {
  height: 300px;
}
.button-div {
  height: 100%;
  width: 100px;
  position: absolute;
  bottom: 0;
  right: 0;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}
.button-item {
  width: 35px;
  height: 35px;
  margin: auto 0;
  border-radius: 8px;
  transition: all 0.1s;
  display: flex;
  /*color: var(--wakuwaku-color-dark);*/
}
.button-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}
.upload-or-like-selector {
  display: flex;
  width: 100%;
  height: 50px;
  line-height: 50px;
  margin: 20px 0;
}
.selector-item {
  width: 50%;
  height: 100%;
  position: relative;
  font-size: 16px;
  font-weight: 600;
}
.selected::after {
  content: '';
  display: block;
  position: absolute;
  bottom: 0;
  width: 80%;
  left: 10%;
  height: 2px;
  background-color: var(--wakuwaku-header-background-color);
  animation: longer 0.2s;
}

@keyframes longer {
  from {
    width: 0;
    left: 50%;
  }
  to {
    width: 80%;
    left: 10%;
  }
}
</style>
