<template>
  <div class="form-item">
    <div class="title">{{ props.title }}</div>
    <waku-input :type="props.type" style="background-color: rgba(0, 0, 0, 0.02); margin: 0; flex-grow: 1;height: 100%;" v-model="ip.val"></waku-input>
  </div>
</template>

<script setup lang="ts">
import {defineProps, reactive, watch} from 'vue'
import WakuInput from "@/components/WakuInput.vue";

const props = defineProps<{
  title : string,
  type : string,
  modelValue: string
}>();

// eslint-disable-next-line no-undef
const emits = defineEmits(['update:modelValue'])

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
.form-item {
  text-align: left;
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 40px;
  margin: 10px 0;
}
.title {
  width: 50px;
  padding-left: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #777777;
}
</style>
