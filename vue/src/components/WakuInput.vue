<template>
  <div class="input-div">
    <slot name="before"></slot>
    <div style="position: relative;">
      <div class="label">{{ ip.val!==''?'' : props.label }}</div>
      <input v-model="ip.val" :type="type" @blur='fnBlur' @input='fnInput'>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, useSlots } from 'vue'

// eslint-disable-next-line no-undef
const props = withDefaults(defineProps<{
  modelValue: string
  label: string
  type: string
}>(), {
  modelValue: '',
  label: '',
  type: 'text'
})
// eslint-disable-next-line no-undef
const emits = defineEmits(['update:modelValue', 'blur', 'input'])

emits('update:modelValue', props.modelValue)

// eslint-disable-next-line no-undef
defineExpose({
  focus: () => {
    const input = document.querySelector('input')
    if (input) {
      input.focus()
    }
  }
})

const fnBlur = () => {
  emits('blur')
}

const fnInput = () => {
  emits('input', ip.val)
}

const ip = reactive({
  val: props.modelValue
})

watch(
    () => props.modelValue,
    (val, preVal) => {
      console.log('modelValue changed')
      ip.val = val
    },
    {}
)

watch(
    () => ip.val,
    (val, preVal) => {
      emits('update:modelValue', val)
    },
    {}
)
</script>

<style scoped>
.input-div {
  position: relative;
  display: flex;
  flex-direction: row;
  height: 40px;
  /*border: 2px solid var(--wakuwaku-color-dark);*/
  border-radius: var(--wakuwaku-medium-radius);
  background-color: var(--wakuwaku-color-light);
  margin-top: 8px;
  margin-bottom: 8px;
  padding: 0 18px;
}
input {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0);
  border: none;
  /*margin: 0 18px;*/
  color: var(--wakuwaku-font-color-dark);
  font-family: inherit;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.25px;
  z-index: 100;
}
input:focus-visible {
  outline: none;
}
.label {
  position: absolute;
  top: 50%;
  padding-left: 3px;
  transform: translate(0, -50%);
  color: var(--wakuwaku-font-color);
  text-align: left;
}
</style>
