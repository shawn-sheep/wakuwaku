<template>
  <div
      class="button-div"
      :class="{
         'disable': !props.enable
      }"
      :style="{
         backgroundColor: props.color? props.color:'var(--wakuwaku-color-spring-grean)',
         '--hover-color': props.hoverColor? props.hoverColor : (props.color? props.color:'var(--wakuwaku-color-spring-grean)')
      }"
      @click="fn"
  >
    <div class="label" :style="{color: props.fontColor? props.fontColor:'white'}">
      <slot name="default"></slot>
    </div>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
const props = defineProps({
  enable: Boolean,
  color: String,
  fontColor: String,
  hoverColor: String
})

// eslint-disable-next-line no-undef
const emit = defineEmits(['click'])

const fn = () => {
  if(props.enable) emit("click")
}
</script>

<style scoped>
.button-div {
  position: relative;
  width: 100%;
  height: 40px;
  margin-top: 8px;
  margin-bottom: 8px;
  background-color: var(--wakuwaku-color-spring-grean);
  border-radius: 999px;
  transition: 0.1s;
  cursor: pointer;
  opacity: 0.7;
  --hover-color: var(--wakuwaku-color-spring-grean);
}
.button-div:not(.disable):hover {
  background-color: var(--hover-color) !important;
  opacity: 1;
}
.label {
  width: 100%;
  position: absolute;
  top: 50%;
  transform: translate(0, -50%);
  color: white;
  font-weight: 800;
}
.disable {
  opacity: 0.2;
}
</style>
