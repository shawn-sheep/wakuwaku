<template>
  <div class="waku-link" @click="goto(route, true)">
    <slot name="default"></slot>
  </div>
</template>

<script setup>
import { goto } from '@/assets/js/api'

// eslint-disable-next-line no-undef
const props = defineProps({
  route: String
})
</script>

<style scoped>
.waku-link {
  transition: all 0.1s;
  width: fit-content;
  cursor: pointer;
}
.waku-link:hover {
  color: #376ea2;
  text-decoration: underline;
}
</style>
