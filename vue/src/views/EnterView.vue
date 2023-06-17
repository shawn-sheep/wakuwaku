<template>
  <div style="padding-top: 30px">
    <WakuButton :enable="true" @click="goto('/register')">注册用户</WakuButton>
    <WakuButton color="var(--wakuwaku-color-light)" font-color="var(--wakuwaku-font-color)" :enable="true" @click="goto('/login')">登录</WakuButton>
  </div>
</template>

<script setup>
import WakuButton from "@/components/WakuButton";
import { goto } from "@/assets/js/api"
</script>
