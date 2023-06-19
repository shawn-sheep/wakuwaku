<template>
  <div style="display: flex;flex-direction: row;justify-content: center;height: 30px">
    <div class="flex-center">
      <slot name="default"></slot>
    </div>
    <div @click="emits('delete')" class="flex-center" style="height: 14px;margin-left: 3px">
      <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>
    </div>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
const emits = defineEmits(['delete'])
</script>

<style scoped>
svg {
  width: 14px;
  height: 14px;
}
.flex-center {
  margin: auto;
}
</style>
