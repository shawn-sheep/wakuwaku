<template>
  <div ref="contentRef" class="image-detail-div" :style="{display: store.state.isDisplayImage?'': 'none'}" @click="handleClick">
    <div
        class="image-content-div"
        :style="{
          width: info.fitType === 'width' ? '75%' : 'auto',
          height: info.fitType === 'height' ? '75%' : 'auto'
        }"
    >
      <waku-static-post
          :img="store.state.displayImage"
          :width="info.postWidth"
      ></waku-static-post>
<!--      <img-->
<!--          v-if="isImage"-->
<!--          :src="store.state.displayImage.src"-->
<!--          :style="{-->
<!--            width: info.fitType === 'width' ? '100%' : '',-->
<!--            height: info.fitType === 'height' ? 'calc(100% - 90px)' : ''-->
<!--          }"-->
<!--      >-->
<!--      <video-->
<!--          v-if="isVideo"-->
<!--          :src="store.state.displayImage.src"-->
<!--          :style="{-->
<!--            width: info.fitType === 'width' ? '100%' : '',-->
<!--            height: info.fitType === 'height' ? 'calc(100% - 90px)' : ''-->
<!--          }"-->
<!--          controls-->
<!--      ></video>-->
      <div class="description-div">
        <div style="text-align: left;font-size: 18px;font-weight: 600;">
          <waku-link style="height: 30px;line-height: 30px">{{ store.state.displayImage.description }}</waku-link>
          <div class="tags-div">
            <waku-tag
                v-for="item in store.state.displayImage.tags"
                v-bind:key="item"
                :name="item.name"
            ></waku-tag>
          </div>
        </div>
        <div class="like-div">
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
  </div>
</template>

<script setup>
import store from "@/store";
import {reactive, ref, watch, computed} from "vue";
import WakuTag from "@/components/WakuTag";
import WakuLink from "@/components/WakuLink";
import WakuButton from "@/components/WakuButton";
import WakuScroller from "@/components/WakuScroller";
import WakuStaticPost from "@/components/WakuStaticPost";

const contentRef = ref(null)

const info = reactive({
  fitType : 'width',
  postWidth : 0
})

const isImage = computed(() => {
  return store.state.displayImage.src.match(/\.(jpg|jpeg|png|gif)$/i)
})

const isVideo = computed(() => {
  return store.state.displayImage.src.match(/\.(mp4|webm|ogg)$/i)
})

const handleClick = () => {
  store.state.isDisplayImage = false
}

watch(
    () => store.state.displayImage,
    (val, preVal) => {
        const whr1 = (window.innerWidth * 0.75) / (window.innerHeight * 0.75 - 90);
        const whr2 = val.width / val.height
        console.log(window.innerWidth)
        console.log(window.innerHeight)
        console.log(whr1)
        console.log(whr2)
        if (whr1 <= whr2) info.fitType = 'width'
        else info.fitType = 'height'
        console.log(info.fitType)
        if (info.fitType === 'width') info.postWidth = window.innerWidth * 0.75;
        else info.postWidth = (window.innerHeight * 0.75 - 90) / val.height * val.width
        console.log(info.postWidth)
    },
    {}
)

</script>

<style scoped>
.image-detail-div {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.5);
  height: 100%;
  width: 100%;
}
.image-content-div {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.description-div {
  width: 100%;
  height: 80px;
  /*background-color: var(--wakuwaku-color-light);*/
  background-color: #FFFFFF;
  border-radius: 20px;
  margin-top: 10px;
  padding: 10px 30px 10px 30px;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.tags-div {
}
.like-div {
  display: flex;
  flex-direction: row;
  justify-content: center;
}
svg {
  width: 20px;
  height: 20px;
}
</style>
