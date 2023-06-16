<template>
  <div>
    <waku-input label="邮箱地址" v-model="form.email" @input="inputCheck"></waku-input>
    <waku-input label="waku ID" v-model="form.account" @input="inputCheck"></waku-input>
    <waku-input label="密码" v-model="form.password" type="password" @input="inputCheck"></waku-input>
    <waku-input label="重复密码" v-model="form.repPassword" type="password" @input="inputCheck"></waku-input>
    <waku-button style="margin-top: 18px" :enable="form.enable" @click="handleRegister">注册</waku-button>
    <div class="error-div">{{ form.errorMessage }}</div>
  </div>
</template>

<script setup>
import WakuInput from "@/components/WakuInput";
import WakuButton from "@/components/WakuButton";
import {reactive} from "vue";
import { register } from "@/assets/js/api";

const form = reactive({
  email: '',
  account: '',
  password: '',
  repPassword: '',
  enable: false,
  errorMessage: ''
})

const inputCheck = () => {
  form.enable = (form.email !== '' && form.account !== '' && form.password !=='' && form.password === form.repPassword)
}

const handleRegister = () => {
  register(form).then((res) => {
    form.errorMessage = res
  })
}
</script>

<style scoped>
.error-div {
  color: indianred;
}
</style>
