<template>
    <div class="waku-button-group">
      <button
        type="button"
        v-for="option in options"
        :key="option.id"
        :class="{ 'active': selectedOptions.includes(option.id) }"
        @click="toggleOption(option.id)"
      >
        {{ option.label }}
      </button>
    </div>
</template>
  
<script setup lang="ts">
import { ref, watch, computed } from 'vue';

// eslint-disable-next-line no-undef
const props = defineProps<{
    type: 'single' | 'multiple';
    options: string[];
    selectedOptions: number[];
}>()

// eslint-disable-next-line no-undef
const emit = defineEmits(['update:selectedOptions'])

const options = computed(() => {
    return props.options.map((option, index) => ({
        id: index,
        label: option,
    }))
})
const selectedOptions = ref(props.selectedOptions)

watch(
    () => props.selectedOptions,
    () => {
      console.log("group options changed")
        selectedOptions.value = props.selectedOptions
    },
    { immediate: true }
)

const toggleOption = (optionId: number) => {
    if (props.type === 'single') {
        selectedOptions.value = [optionId]
    } else {
        const index = selectedOptions.value.indexOf(optionId)
        if (index === -1) {
            selectedOptions.value.push(optionId)
        } else {
            selectedOptions.value.splice(index, 1)
        }
    }
    emit('update:selectedOptions', selectedOptions.value)
}
</script>
  
<style scoped>

.waku-button-group {
  display: flex;
  flex-direction: row;
}

.waku-button-group button {
  background-color: #fff;
  border: 0;
  border-radius: 10px;
  color: var(--wakuwaku-font-color-dark);
  cursor: pointer;
  font-size: 14px;
  margin: 0 10px;
  padding: 10px 15px;
  transition: all 0.2s ease-in-out;
}

.waku-button-group button:hover {
  color: var(--wakuwaku-header-font-color);
}

.waku-button-group button.active {
  background-color: var(--wakuwaku-searchbar-hover-background-color);
  color: var(--wakuwaku-header-font-color);
}
</style>
  