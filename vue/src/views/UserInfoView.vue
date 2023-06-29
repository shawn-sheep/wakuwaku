<template>
  <div>
    <div style="background-color: rgba(0 ,0 ,0, 0.02);padding: 20px 0 20px 0">
      <div class="post-upload" v-if="info.avatar_url === undefined">
        <div style="height: 50px"></div>
        <waku-button style="width: 200px;" :enable="true" >
          <input class="file-btn" type="file" @change="setImage">
          上传头像
        </waku-button>
        <div style="font-size: 12px;font-weight: 500">请上传JPEG/PNG文件</div>
      </div>
      <div style="position: relative;width: 250px;margin: auto" v-if="info.avatar_url !== undefined">
        <div style="position: absolute;right: 0;z-index: 2;padding: 0 10px;background-color: rgba(0, 0, 0, 0.4);border-bottom-left-radius: 8px">
          <waku-deletable-item style="color: #EEEEEE;font-size: 12px" @delete="onDelete">{{ file?.name }}</waku-deletable-item>
        </div>
        <waku-avatar :src="info.avatar_url" :size="200" style="margin: auto"></waku-avatar>
      </div>
    </div>
    <div class="information-div">
      <waku-form-item title="用户名" v-model="info.username" style="padding: 10px 0"></waku-form-item>
      <waku-form-item title="邮箱" v-model="info.email" style="padding: 10px 0"></waku-form-item>
      <waku-button style="width: 200px;margin:20px auto" color="#376ea2" :enable="true" @click="onSubmit">修改</waku-button>
      <div style="height: 200px;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import WakuButton from "@/components/WakuButton.vue"
import WakuFormItem from "@/components/WakuFormItem.vue";
import WakuDeletableItem from "@/components/WakuDeletableItem.vue";
import WakuAvatar from "@/components/WakuAvatar.vue";
import { updateUserInfo, goto } from "@/assets/js/api";
import store from "@/store";

const info = reactive<{
  username : string,
  email : string,
  avatar_url : string | undefined
}>({
  username: '',
  email: '',
  avatar_url: undefined
})

watch(() => store.state.user, (user) => {
  // 异步更新
  setTimeout(() => {
    info.username = user.username;
    info.email = user.email;
    info.avatar_url = user.avatar_url;
  }, 0)
}, { immediate: true })

const file = ref<File>();
const setImage = (event : Event) => {
  console.log(event.target?.files[0])
  file.value = event.target?.files[0];
  if (!file.value) return;
  // 中心裁剪
  const reader = new FileReader();
  reader.readAsDataURL(file.value);
  reader.onload = () => {
    const img = new Image();
    img.src = reader.result as string;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const width = img.width;
      const height = img.height;
      const size = Math.min(width, height);
      canvas.width = size;
      canvas.height = size;
      ctx?.drawImage(img, (width - size) / 2, (height - size) / 2, size, size, 0, 0, size, size);
      const dataURL = canvas.toDataURL('image/jpeg');
      info.avatar_url = dataURL;
    }
  }
}

const onDelete = () => {
  info.avatar_url = undefined;
}

const onSubmit = async () => {
  let form : any = {};
  if (!info.username) {
    alert('用户名不能为空');
    return;
  }
  if (!info.email) {
    alert('邮箱不能为空');
    return;
  }
  if (info.username !== store.state.user.username) {
    form['username'] = info.username;
  }
  if (info.email !== store.state.user.email) {
    form['email'] = info.email;
  }
  if (file.value) {
    form['avatar'] = file.value;
  }
  const res = await updateUserInfo(form);
  if (res.message == 'user updated successfully') {
    goto('/user/' + store.state.user.account_id);
    // 刷新页面
    setTimeout(() => {
      location.reload();
    }, 0)
  } else {
    alert(`修改失败：${res.message}`)
  }
}

</script>

<style scoped>
.post-upload {
  height: 200px;
}
.post-upload div {
  margin: 10px auto;
}
.information-div {
  max-width: 600px;
  margin: 20px auto 0 auto;
}
.file-btn {
  position: absolute;
  width: 100%;
  height: 40px;
  bottom: -12px;
  left: 0;
  outline: none;
  filter: alpha(opacity=0);
  opacity: 0;
  cursor: pointer;
}
.title-description-div {
  padding: 10px 0;
}
</style>
