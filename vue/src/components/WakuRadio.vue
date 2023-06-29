<template>
  <div class="audio-div" :class="{'selected' : props.modelValue === props.value}" @click="emits('update:modelValue', props.value)">
    <div class="pointer">
      <div class="inner-pointer"></div>
    </div>
    {{ props.name }}
  </div>
</template>

<script setup lang="ts">
// eslint-disable-next-line no-undef
const props = defineProps<{
  name : string,
  value : string,
  modelValue : string
}>()

// eslint-disable-next-line no-undef
const emits = defineEmits(['update:modelValue'])
</script>

<style scoped>
.audio-div {
  font-size: 16px;
  font-weight: 600;
  color: #777777;
  padding: 0 10px;
  cursor: pointer;
}
.pointer {
  display: inline-block;
  position: relative;
  width: 12px;
  height: 12px;
  border: #AAAAAA 2px solid;
  box-sizing: border-box;
  border-radius: 999px;
  margin-right: 5px;
  vertical-align: -5%;
}
.inner-pointer {
  position: absolute;
  background-color: #42b983;
  border-radius: 999px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: height,width 0.1s;
}
.selected {
  color: #42b983;
}
.selected .pointer {
  border: #42b983 2px solid;
}
.selected .inner-pointer {
  height: 6px;
  width: 6px;
}
</style>
