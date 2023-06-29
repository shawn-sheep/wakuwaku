<template>
  <div class="input-div">
    <slot name="before"></slot>
    <div style="position: relative;flex-grow: 1">
      <div class="label">{{ ip.val!==''?'' : props.label }}</div>
      <input v-model="ip.val" :type="type" @blur='fnBlur' @input='fnInput' v-if="props.type !== 'text-area'">
      <textarea v-model="ip.val" @blur='fnBlur' @input='fnInput' v-if="props.type === 'text-area'"></textarea>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, useSlots } from 'vue'

// eslint-disable-next-line no-undef
const props = defineProps({
  modelValue: String,
  label: String,
  type: String
})
// eslint-disable-next-line no-undef
const emits = defineEmits(['update:modelValue', 'blur', 'input'])

const fnBlur = () => {
  emits('blur')
}

const fnInput = () => {
  emits('input')
}

const ip = reactive({
  val: ''
})

watch(
    () => props.modelValue,
    (val, preVal) => {
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
input, textarea {
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
textarea {
  resize: none;
  margin: 10px 0;
  height: calc(100% - 20px);
}
input:focus-visible, textarea:focus-visible {
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
