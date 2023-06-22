<template>
  <div class="toolbar-item">
    <slot name="default"></slot>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
const props = defineProps({
  route: String
})
</script>

<style scoped>
.toolbar-item {
  height: 100%;
  padding-left: 10px;
  padding-right: 10px;
  transition: 0.1s;
  cursor: pointer;
}
.toolbar-item:hover {
  background-color: var(--wakuwaku-header-font-color);
  color: var(--wakuwaku-header-background-color);
}
</style>
