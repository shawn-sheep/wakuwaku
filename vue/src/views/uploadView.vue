<template>
  <div>
    <div style="background-color: rgba(0 ,0 ,0, 0.02);padding: 20px 0 20px 0">
      <div class="post-upload" v-if="form.images === undefined">
        <div style="height: 50px"></div>
        <waku-button style="width: 200px;" :enable="true" >
          <input class="file-btn" type="file" @change="setImage">
          上传图片
        </waku-button>
        <div style="font-size: 12px;font-weight: 500">请上传JPEG/PNG文件</div>
      </div>
      <div style="position: relative;width: 60%;margin: auto" v-if="form.images !== undefined">
        <div style="position: absolute;right: 0;z-index: 2;padding: 0 10px;background-color: rgba(0, 0, 0, 0.4);border-bottom-left-radius: 8px">
          <waku-deletable-item style="color: #EEEEEE;font-size: 12px" @delete="onDelete">{{ file.name }}</waku-deletable-item>
        </div>
        <waku-static-post :img="form.images" style="border-radius: 0px"></waku-static-post>
      </div>
    </div>
    <div class="information-div">
      <div class="title-description-div">
        <waku-form-item title="标题" v-model="form.title"></waku-form-item>
        <waku-form-item title="简介" type="text-area" style="height: 80px" v-model="form.content"></waku-form-item>
      </div>
      <waku-form-item title="来源" v-model="form.source" style="padding: 10px 0"></waku-form-item>
      <div class="rating-div">
        <div class="rating-item">分级</div>
        <waku-audio style="margin: auto 0" name="General" value="G" v-model="form.rating"></waku-audio>
        <waku-audio style="margin: auto 0" name="Sensitive" value="S" v-model="form.rating"></waku-audio>
        <waku-audio style="margin: auto 0" name="Questionable" value="Q" v-model="form.rating"></waku-audio>
        <waku-audio style="margin: auto 0" name="Explicit" value="E" v-model="form.rating"></waku-audio>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {reactive, ref} from "vue";
import {image} from "@/assets/js/api";
import WakuStaticPost from "@/components/WakuStaticPost.vue";
import WakuButton from "@/components/WakuButton.vue"
import WakuInput from "@/components/WakuInput.vue";
import WakuFormItem from "@/components/WakuFormItem.vue";
import WakuAudio from "@/components/WakuAudio.vue";
import WakuDeletableItem from "@/components/WakuDeletableItem.vue";

const form = reactive<{
  images? : image,
  title : string,
  content : string,
  source: string,
  rating: string
}>({
  images : undefined,
  title: '',
  content: '',
  source: '',
  rating: 'G'
})

const file = ref<File>();
const setImage = (event : Event) => {
  console.log(event.target?.files[0])
  file.value = event.target?.files[0];
  if (!file.value) return;
  form.images = new image()
  // console.log(file.webkitRelativePath)
  form.images.sample_url = window.URL.createObjectURL(file.value);
  console.log(form.images.sample_url)
  // const reader = new FileReader();
  // reader.readAsDataURL(file);
  // reader.onload = () => {
  //   form.images = reader.result
  //   console.log(form.images)
  // }
}

const onDelete = () => {
  form.images = undefined;
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
}
.title-description-div {
  padding: 10px 0;
}
.rating-div {
  height: 40px;
  padding: 10px 0;
  display: flex;
  flex-direction: row;
  text-align: left;
}
.rating-item {
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
