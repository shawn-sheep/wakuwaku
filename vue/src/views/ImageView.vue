<template>
  <div style="background-color: rgba(0, 0, 0, 0.04); padding: 20px">
    <div style="border-radius: 10px;overflow: hidden;background-color: #FFFFFF">
      <waku-static-post :img="info.img" style="border-radius: 0"></waku-static-post>
      <div class="information-div">
        <div class="like-div">
          <div style="display: inline-block">
            <div style="display: flex;flex-direction: row;text-align: center;gap: 10px">
              <waku-button color="#FFFFFF" hover-color="rgba(0,0,0,0.4)" font-color="#000000" style="width: 40px" :enable="true">
                <div style="display: inline-block;height: 20px;vertical-align: baseline">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="CurrentColor"><path d="M5 22h-5v-12h5v12zm17.615-8.412c-.857-.115-.578-.734.031-.922.521-.16 1.354-.5 1.354-1.51 0-.672-.5-1.562-2.271-1.49-1.228.05-3.666-.198-4.979-.885.906-3.656.688-8.781-1.688-8.781-1.594 0-1.896 1.807-2.375 3.469-1.221 4.242-3.312 6.017-5.687 6.885v10.878c4.382.701 6.345 2.768 10.505 2.768 3.198 0 4.852-1.735 4.852-2.666 0-.335-.272-.573-.96-.626-.811-.062-.734-.812.031-.953 1.268-.234 1.826-.914 1.826-1.543 0-.529-.396-1.022-1.098-1.181-.837-.189-.664-.757.031-.812 1.133-.09 1.688-.764 1.688-1.41 0-.565-.424-1.109-1.26-1.221z"/></svg>
                </div>
              </waku-button>
              <waku-button color="#FFFFFF" hover-color="rgba(0,0,0,0.4)" font-color="#000000" style="width: 40px" :enable="true">
                <div style="display: inline-block;height: 20px;vertical-align: bottom">
                  <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" fill="CurrentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 5.72c-2.624-4.517-10-3.198-10 2.461 0 3.725 4.345 7.727 9.303 12.54.194.189.446.283.697.283s.503-.094.697-.283c4.977-4.831 9.303-8.814 9.303-12.54 0-5.678-7.396-6.944-10-2.461z" fill-rule="nonzero"/></svg>
                </div>
              </waku-button>
            </div>
          </div>
        </div>
        <div class="description-div">{{ info.img.description !== '' ? info.img.description : '无题' }}</div>
        <div class="tag-div">
          <waku-tag v-for="tag in info.img.tags" :key="tag" :tag="tag"></waku-tag>
        </div>
        <div class="rect-div">{{ info.img.width + 'x' + info.img.height }}</div>
        <div style="margin: 20px 0; height: 2px;background-color: #AAAAAA"></div>
        <div style="display: flex;flex-direction: row;margin: 20px 0;gap: 20px">
          <waku-avatar :src="store.state.user.avatar" :size="40" style="margin: auto 0"></waku-avatar>
          <waku-input style="background-color: rgba(0, 0, 0, 0.02);width: 100%" label="发表评论"></waku-input>
          <waku-button style="width: 100px;text-align: center" :enable="true">发送</waku-button>
        </div>
        <div class="commits-div">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {defineProps, onMounted, reactive, ref, watch} from 'vue'
import {getImageByID, image} from "@/assets/js/api";
import WakuStaticPost from "@/components/WakuStaticPost.vue";
import WakuTag from "@/components/WakuTag.vue"
import WakuButton from "@/components/WakuButton.vue"
import WakuInput from "@/components/WakuInput.vue";
import WakuAvatar from "@/components/WakuAvatar.vue";
import store from "@/store"
const props = defineProps<{
  id : string
}>()

const info = reactive<{
  img : image
}>({
  img : new image()
})

onMounted(() => {
  watch(
      () => props.id,
      (val, oldVal) => {
        updateImage(val)
      },
      {
        immediate: true
      }
  )
})

const updateImage = (id : string) => {
  getImageByID(id).then((res) => {
    info.img = res
    console.log(info.img)
  })
}
</script>

<style scoped>
.information-div {
  width: 700px;
  margin: auto;
  text-align: left;
}
.like-div {
  height: 40px;
  text-align: right;
  margin: 20px 0;
}
.description-div {
  font-size: 24px;
  margin: 20px 0;
  font-weight: 800;
}
.tag-div {
  font-weight: 500;
  font-size: 16px;
  line-height: 22px;
  margin: 20px 0;
}
.rect-div {
  color: rgba(0, 0, 0, 0.4);
  font-size: 12px;
  margin: 20px 0;
}
svg {
  width: 20px;
  height: 20px;
}
</style>
