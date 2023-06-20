<template>
  <div class="search-div">
    <div class="search-bar">
      <div class="search-form" @click="onClick" @focusout="onFocusOut">
        <svg width="24" height="24" stroke="CurrentColor" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 38C30.3888 38 38 30.3888 38 21C38 11.6112 30.3888 4 21 4C11.6112 4 4 11.6112 4 21C4 30.3888 11.6112 38 21 38Z" fill="none" stroke-width="4" stroke-linejoin="round"/><path d="M26.657 14.3431C25.2093 12.8954 23.2093 12 21.0001 12C18.791 12 16.791 12.8954 15.3433 14.3431" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M33.2216 33.2217L41.7069 41.707" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <input type="text" placeholder="Search"
        @input="onInput" ref="input"
        @keydown.down="onKeyDown"
        @keydown.up="onKeyUp"
        @keydown.enter="onEnter"
        @keydown.tab="onTab"
        />
      </div>
      <transition name="search-panel">
      <div class="search-panel" v-if="isFocus" @mouseenter="selectPanel = true" @mouseleave="selectPanel = false">
        <div v-for="item, index in autoCompletes" :key="index"
          :class="['search-panel-item', {'selected': selectedIndex === index}]"
          @click="onSelected(item)"
          @mouseenter="onMouseEnter(index)">
          {{item.name}}
        </div>
      </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import { tag, autoComplete, goto } from '@/assets/js/api';
import { useRoute } from "vue-router";
import { onMounted } from 'vue';

const isFocus = ref(false)
const selectPanel = ref(false)
const selectedIndex = ref(-1)

const input = ref<HTMLInputElement>()

const autoCompletes = ref<tag[]>([])

// 根据路由中tags参数，初始化搜索框
onMounted(() => {
  const route = useRoute()
  const tags = route.query.tags
  if (tags) {
    input.value!.value = tags as string
    onInput({target: input.value!})
  }
})

const onClick = (e: any) => {
  input.value!.focus()
  isFocus.value = true
  onInput({target: input.value!})
}

const onFocusOut = (e: any) => {
  if (!selectPanel.value) {
    isFocus.value = false
  }
}

const onInput = (e: any) => {
  console.log('onInput', e.target.value)
  // 补全最后一词
  const value = e.target.value
  const index = value.lastIndexOf(' ')
  const lastWord = value.substring(index + 1)
  autoComplete(lastWord).then(res => {
    autoCompletes.value = res
    selectedIndex.value = -1
  })
}

const onKeyDown = (e: any) => {
  e.preventDefault()
  if (selectedIndex.value < autoCompletes.value.length - 1) {
    selectedIndex.value += 1
  }
}

const onKeyUp = (e: any) => {
  e.preventDefault()
  if (selectedIndex.value > 0) {
    selectedIndex.value -= 1
  }
}

const onTab = (e: any) => {
  e.preventDefault()
  if (selectedIndex.value >= 0) {
    onSelected(autoCompletes.value[selectedIndex.value])
  }
}

const onEnter = (e: any) => {
  if (selectedIndex.value >= 0) {
    onSelected(autoCompletes.value[selectedIndex.value])
    goto('/search?tags=' + input.value!.value)
  }
}

const onSelected = (item: tag) => {
  console.log('onSelect', item)
  input.value!.focus()
  isFocus.value = true
  // 补全最后一个
  const value = input.value!.value
  const index = value.lastIndexOf(' ')
  input.value!.value = value.substring(0, index + 1) + item.name
}

const onMouseEnter = (index: number) => {
  selectedIndex.value = index
}

</script>

<style scoped>

.search-panel-enter-active {
  animation: search-panel 0.2s;
}

.search-panel-leave-active {
  animation: search-panel 0.2s reverse;
}

@keyframes search-panel {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-div {
  width: 100%;
  height: 34px;
  position: relative;
  background: var(--wakuwaku-searchbar-background-color);
  border-radius: 999px;
}

.search-bar {
  top: 0;
  width: 100%;
  height: auto;
  position: absolute;
  background: var(--wakuwaku-searchbar-background-color);
  border-radius: 15px;
  overflow: hidden;
  transition: border 0.1s;
  border: 2px solid rgba(0, 0, 0, 0);
}

/* 判断是否为搜索状态 */
.search-bar:hover, .search-bar:focus-within {
  border: 2px solid var(--wakuwaku-searchbar-border-color);
}

.search-form {
  width: 100%;
  height: 30px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.search-panel {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
}

.search-panel-item {
  padding: 0 10px;
  width: 100%;
  height: 30px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

/* 同时为item且sleected */
.search-panel-item.selected {
  background: var(--wakuwaku-searchbar-hover-background-color);
}

input {
  position: relative;
  width: calc(100% - 30px);
  height: 100%;
  background-color: rgba(0,0,0,0);
  border: none;
  margin: auto;
  color: inherit;
  font-family: inherit;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.25px;
  z-index: 100;
  top: -0.5px;
}
input:focus-visible {
  outline: none;
}
input::-webkit-input-placeholder {
  color: inherit;
  opacity: 0.7;
}
svg {
  width: 20px;
  height: 20px;
  padding-left: 10px;
  padding-right: 5px;
}
</style>
