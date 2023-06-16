<template>
  <div style="position: absolute;width: 100%;height: 100%;background: var(--wakuwaku-main-background-color);">
    <div class="header">
      <HeaderBar></HeaderBar>
    </div>
    <div class="main">
      <waku-scroller style="height: 100%;width: 100%" scroll-direction="column">
        <div style="height: 100%;width: 100%;box-sizing: border-box;padding: 20px">
          <router-view></router-view>
        </div>
      </waku-scroller>
    </div>
  </div>
</template>

<script setup>
import HeaderBar from "@/components/HeaderBar";
import WakuScroller from "@/components/WakuScroller";
</script>

<style scoped>
.header {
  height: 50px;
  width: 100%;
  position: fixed;
  background: var(--wakuwaku-header-background-color);
}
.main {
  padding-top: 50px;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}
</style>
