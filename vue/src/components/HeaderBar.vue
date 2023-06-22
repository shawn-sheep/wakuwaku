<template>
  <div class="header-bar">
    <div style="font-weight: 800; font-size: 20px;padding-left: 40px;">
      <div style="padding-right: 20px; cursor: pointer" @click="goto('/home')">WAKUWAKU</div>
      <div class="tool-bar">
        <tool-bar-item>插画</tool-bar-item>
        <tool-bar-item @click="goto('/tags')">标签</tool-bar-item>
        <tool-bar-item>作者</tool-bar-item>
        <tool-bar-item>排行榜</tool-bar-item>
      </div>
    </div>
    <div style="flex: 1; margin-right: 20px;max-width: 500px;">
      <search-bar></search-bar>
    </div>
    <div>
      <headbar-avatar :username="store.state.user.username"></headbar-avatar>
    </div>
  </div>
</template>

<script setup>
import ToolBarItem from "@/components/ToolBarItem";
import SearchBar from "@/components/SearchBar";
import HeadbarAvatar from "@/components/HeadbarAvatar";
import store from "@/store";
import { goto } from  "@/assets/js/api"
</script>

<style scoped>
.header-bar {
  height: 100%;
  display: flex;
  flex-direction: row;
  position: relative;
  justify-content: space-between;
  color: var(--wakuwaku-header-font-color);
}
.header-bar div {
  position: relative;
  display: flex;
  align-items: center;
  flex-direction: row;
}
.tool-bar {
  height: 100%;
  font-size: 14px;
  font-weight: 800;
  padding-right: 20px;
}
</style>
