<template>
  <div class="headbar-avatar-div">
    <div style="font-size: 18px; font-weight: 600">{{ props.username }}</div>
    <WakuAvatar :src="store.state.user.avatar" :size="38" style="padding-left: 10px;padding-right: 20px"></WakuAvatar>
  </div>
</template>

<script setup>
import WakuAvatar from "@/components/WakuAvatar";
import store from "@/store";
// eslint-disable-next-line no-undef
const props = defineProps({
  username: String
})
</script>

<style scoped>
.headbar-avatar-div {
  display: flex;
  flex-direction: row;
}
</style>
