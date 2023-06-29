<template>
  <div>
    <div style="background-color: rgba(0 ,0 ,0, 0.02);padding: 20px 0 20px 0">
      <div class="post-upload" v-if="info.images === undefined">
        <div style="height: 50px"></div>
        <waku-button style="width: 200px;" :enable="true" >
          <input class="file-btn" type="file" @change="setImage">
          上传图片
        </waku-button>
        <div style="font-size: 12px;font-weight: 500">请上传JPEG/PNG文件</div>
      </div>
      <div style="position: relative;width: 60%;margin: auto" v-if="info.images !== undefined">
        <div style="position: absolute;right: 0;z-index: 2;padding: 0 10px;background-color: rgba(0, 0, 0, 0.4);border-bottom-left-radius: 8px">
          <waku-deletable-item style="color: #EEEEEE;font-size: 12px" @delete="onDelete">{{ file?.name }}</waku-deletable-item>
        </div>
        <waku-static-post :img="info.images" style="border-radius: 0px"></waku-static-post>
      </div>
    </div>
    <div class="information-div">
      <div class="title-description-div">
        <waku-form-item title="标题" v-model="info.title"></waku-form-item>
        <waku-form-item title="简介" type="text-area" style="height: 120px" v-model="info.content"></waku-form-item>
      </div>
      <div ref="tagRef" style="padding: 10px 0;position: relative">
        <waku-form-item title="标签" v-model="info.search" type=""></waku-form-item>
        <div class="auto-complete" v-if="visible" v-click-outside:[tagRef]="fn">
          <div class="auto-complete-item" v-for="item in autoCompletes" :key="item.tag_id" @click.stop="insertTag(item)">{{ item.name }}</div>
        </div>
        <div class="tags-div">
          <div style="display: inline-block;background-color: rgba(0, 0, 0, 0.4);color: #FFFFFF;border-radius: 5px; margin-right: 10px" v-for="item in info.tags" :key="item.tag_id">
            <waku-deletable-item  @delete="deleteTag(item)" style="padding: 5px 10px;height: auto;gap: 5px;">{{ item.name }}</waku-deletable-item>
          </div>
        </div>
      </div>
      <waku-form-item title="来源" v-model="info.source" style="padding: 10px 0"></waku-form-item>
      <div class="rating-div">
        <div class="rating-item">分级</div>
        <waku-radio style="margin: auto 0" name="General" value="g" v-model="info.rating"></waku-radio>
        <waku-radio style="margin: auto 0" name="Sensitive" value="s" v-model="info.rating"></waku-radio>
        <waku-radio style="margin: auto 0" name="Questionable" value="q" v-model="info.rating"></waku-radio>
        <waku-radio style="margin: auto 0" name="Explicit" value="e" v-model="info.rating"></waku-radio>
      </div>
      <waku-button style="width: 200px;margin:20px auto" color="#376ea2" :enable="true" @click="onSubmit">上传</waku-button>
      <div style="height: 200px;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {reactive, ref, watch} from "vue";
import {autoComplete, image, tag} from "@/assets/js/api";
import WakuStaticPost from "@/components/WakuStaticPost.vue";
import WakuButton from "@/components/WakuButton.vue"
import WakuFormItem from "@/components/WakuFormItem.vue";
import WakuRadio from "@/components/WakuRadio.vue";
import WakuDeletableItem from "@/components/WakuDeletableItem.vue";
import { createPost, goto } from "@/assets/js/api";

const info = reactive<{
  images? : image,
  title : string,
  content : string,
  source: string,
  rating: string,
  search: string,
  tags: tag[],
}>({
  images : undefined,
  title: '',
  content: '',
  source: '',
  rating: 'g',
  search: '',
  tags: []
})

const autoCompletes = ref<tag[]>()
const visible = ref<boolean>(false)
const tagRef = ref<Element>()

const file = ref<File>();
const setImage = (event : Event) => {
  console.log(event.target?.files[0])
  file.value = event.target?.files[0];
  if (!file.value) return;
  info.images = new image()
  // console.log(file.webkitRelativePath)
  info.images.sample_url = window.URL.createObjectURL(file.value);
  console.log(info.images.sample_url)
  // const reader = new FileReader();
  // reader.readAsDataURL(file);
  // reader.onload = () => {
  //   form.images = reader.result
  //   console.log(form.images)
  // }
}

const insertTag = (tag : tag) => {
  info.tags.push(tag);
  visible.value = false
}

const deleteTag = (tag : tag) => {
  info.tags.splice(info.tags.findIndex((item) => {
    return item == tag;
  }), 1);
  visible.value = false
}

const onDelete = () => {
  info.images = undefined;
}

const onInput = () => {
  console.log('onInput', info.search)
  visible.value = true;
  // 补全最后一词
  const index = info.search.lastIndexOf(' ')
  const lastWord = info.search.substring(index + 1)
  autoComplete(lastWord).then(res => {
    autoCompletes.value = res
  })
}

const onSubmit = async () => {
  if (!file.value) {
    alert('请选择文件')
    return
  }
  const form = {
    title: info.title,
    content: info.content,
    source: info.source,
    rating: info.rating,
    tags: info.tags.map(item => item.name).join(' '),
    images: [file.value],
  }
  const res = await createPost(form)
  if (res.message == 'post created successfully') {
    goto('/post/' + res.post_id)
  } else {
    alert(`上传失败：${res.message}`)
  }
}
watch(
    () => info.search,
    (val, oldVal) => {
      onInput()
    },
    {}
)

const fn = () => {
  visible.value = false
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
.auto-complete {
  position: absolute;
  left: 60px;
  width: calc(100% - 60px);
  background-color: #FAFAFA;
  z-index: 2;
  border-radius: 5px;
  text-align: left;
  overflow: hidden;
}
.auto-complete-item {
  height: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.1s;
  padding-left: 20px;
}
.auto-complete-item:hover {
  background-color: rgba(0, 0, 0, 0.2);
}
.tags-div {
  padding-left: 60px;
  width: calc(100% - 60px);
  text-align: left;
}
</style>
