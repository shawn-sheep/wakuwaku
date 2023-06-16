<template>
  <div>
    <waku-input label="邮箱地址或waku ID" v-model="form.account" @input="inputAccount"></waku-input>
    <waku-input label="密码" type="password" v-model="form.password" @input="inputPassword"></waku-input>
    <waku-button :enable="form.enable" style="margin-top: 18px" @click="handleLogin">登录</waku-button>
    <div class="error-div"> {{ form.errorMessage }} </div>
  </div>
</template>

<script setup>
import WakuInput from "@/components/WakuInput";
import WakuButton from "@/components/WakuButton";
import {reactive} from "vue";
import { login } from "@/assets/js/api";

const form = reactive({
  account: '',
  password: '',
  enable: false,
  errorMessage: ''
})

const inputAccount = () => {
  form.enable = (form.account !== '' && form.password !== '')
}

const inputPassword = () => {
  form.enable = (form.account !== '' && form.password !== '')
}

const handleLogin = () => {
  login(form).then((res) => {
    form.errorMessage = res
  })
}
</script>

<style scoped>
.error-div {
  color: indianred;
}
</style>
