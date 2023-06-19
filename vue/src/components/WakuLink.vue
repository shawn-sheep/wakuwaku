<template>
  <div class="waku-link" @click="onClick">
    <slot name="default"></slot>
  </div>
</template>

<script setup>
import { goto } from '@/assets/js/api'

// eslint-disable-next-line no-undef
const props = defineProps({
  route: String
})

const onClick = () => {
  if(props.route != null)
    goto(props.route, true)
}
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
