<template>
  <div ref="contentRef" class="image-detail-div" :style="{display: store.state.isDisplayImage?'': 'none'}" @click="handleClick">
    <div class="image-content-div">
      <waku-link :route="'/post/' + store.state.displayPost.post_id" style="margin: 0 auto">
        <waku-static-post
            :img="store.state.displayPost.imgs[0]"
            :width="info.postWidth"
        ></waku-static-post>
      </waku-link>
      <div class="description-div" @click.stop="">
        <div class="information-div" style="">
          <waku-link style="height: 30px;line-height: 30px" :route="'/post/' + store.state.displayPost.post_id">{{ store.state.displayPost.title !== '' ? store.state.displayPost.title : '无题' }}</waku-link>
          <div class="tags-div">
            <waku-tag
                v-for="item in store.state.displayPost.tags"
                v-bind:key="item"
                :tag="item"
            ></waku-tag>
          </div>
        </div>
        <div class="like-div">
          <waku-button color="#FFFFFF" hover-color="rgba(0,0,0,0.4)" :font-color="store.state.displayPost.self_vote ? '#FF4A80' : '#000000'" style="width: 40px" :enable="true" @click="onLikeClick">
            <div style="display: inline-block;height: 20px;vertical-align: baseline">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="CurrentColor"><path d="M5 22h-5v-12h5v12zm17.615-8.412c-.857-.115-.578-.734.031-.922.521-.16 1.354-.5 1.354-1.51 0-.672-.5-1.562-2.271-1.49-1.228.05-3.666-.198-4.979-.885.906-3.656.688-8.781-1.688-8.781-1.594 0-1.896 1.807-2.375 3.469-1.221 4.242-3.312 6.017-5.687 6.885v10.878c4.382.701 6.345 2.768 10.505 2.768 3.198 0 4.852-1.735 4.852-2.666 0-.335-.272-.573-.96-.626-.811-.062-.734-.812.031-.953 1.268-.234 1.826-.914 1.826-1.543 0-.529-.396-1.022-1.098-1.181-.837-.189-.664-.757.031-.812 1.133-.09 1.688-.764 1.688-1.41 0-.565-.424-1.109-1.26-1.221z"/></svg>
            </div>
          </waku-button>
          <waku-button color="#FFFFFF" hover-color="rgba(0,0,0,0.4)" :font-color="store.state.displayPost.self_fav ? '#FF4A80' : '#000000'" style="width: 40px" :enable="true" @click="onFavoriteClick">
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
import {vote, favorite} from "@/assets/js/api";

const contentRef = ref(null)

const info = reactive({
  fitType : 'width',
  postWidth : 0
})

const handleClick = () => {
  store.state.isDisplayImage = false
}

watch(
    () => store.state.displayPost,
    (val, preVal) => {
        // console.log(store.state.displayImage)
        const whr1 = (window.innerWidth * 0.75) / (window.innerHeight * 0.75 - 90);
        const whr2 = val.imgs[0].width / val.imgs[0].height
        // console.log(window.innerWidth)
        // console.log(window.innerHeight)
        // console.log(whr1)
        // console.log(whr2)
        if (whr1 <= whr2) info.fitType = 'width'
        else info.fitType = 'height'
        // console.log(info.fitType)
        if (info.fitType === 'width') info.postWidth = window.innerWidth * 0.75;
        else info.postWidth = (window.innerHeight * 0.75 - 90) / val.imgs[0].height * val.imgs[0].width
        // console.log(info.postWidth)
        console.log(val)
    },
    {}
)

const onLikeClick = () => {
  console.log('like')
  store.state.displayPost.self_vote = store.state.displayPost.self_vote === 1 ? 0 : 1
  vote(store.state.displayPost.post_id, store.state.displayPost.self_vote ? 'up' : 'cancel')
}

const onFavoriteClick = () => {
  console.log('favorite')
  store.state.displayPost.self_fav = !store.state.displayPost.self_fav
  favorite(store.state.displayPost.post_id, store.state.displayPost.self_fav)
}

</script>

<style scoped>
.image-detail-div {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.5);
  height: 100%;
  width: 100%;
  z-index: 2;
}
.image-content-div {
  width: 75%;
  height: 75%;
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
.information-div {
  text-align: left;
  font-size: 18px;
  font-weight: 600;
  width: calc(100% - 100px);
  position: relative;
}
.information-div::before {
  content: '';
  display: block;
  position: absolute;
  height: 100%;
  width: 100%;
  pointer-events: none;
  background-image: linear-gradient(to right, rgba(255, 255, 255, 0) 92%, rgba(255, 255, 255, 1));
}
.tags-div {
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
}
.like-div {
  width: 100px;
  display: flex;
  flex-direction: row;
  justify-content: center;
}
svg {
  width: 20px;
  height: 20px;
}
</style>
