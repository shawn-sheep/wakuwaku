<template>
  <div style="width: 100%; height: 100%; background-color: var(--wakuwaku-background-color); position: absolute">
    <div class="login-div">
      <div class="logo-text">WAKUWAKU</div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import {onMounted} from "vue";
import {checkLogin} from "@/assets/js/api";

onMounted(() => {
  checkLogin()
})
</script>

<style scoped>
  .login-div {
    width: 300px;
    min-height: 300px;
    position: absolute;
    transform: translate(-50%, -50%);
    top: 50%;
    left: 50%;
    background-color: white;
    border-radius: var(--wakuwaku-large-radius);
    box-sizing: border-box;
    padding: 30px 35px 30px 35px;
  }
  .logo-text {
    width: 100%;
    font-size: 20px;
    font-weight: 800;
    padding-bottom: 25px;
  }
</style>
