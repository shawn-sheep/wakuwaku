<template>
  <div :style="{width: props.size+'px', height: props.size+'px'}">
    <div style="border-radius: 999px;overflow: hidden" :style="{width: props.size+'px', height: props.size+'px'}">
      <img :src="props.src ? props.src : require('@/assets/img/user_avatar.jpg')" style="width: 100%;">
    </div>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
const props = defineProps({
  src : String,
  size : Number
})
</script>

<style scoped>

</style>
