<template>
  <div style="background-color: rgba(0, 0, 0, 0.04); padding: 20px">
    <div style="border-radius: 10px;overflow: hidden;background-color: #FFFFFF">
      <waku-static-post :img="info.post.imgs[0]" class="post-div" @click="goto(info.post.imgs[0].original_url, true, false)"></waku-static-post>
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
        <div class="title-div">{{ info.post.title !== '' ? info.post.title : '无题' }}</div>
        <div class="content-div" v-html="info.post.content"></div>

        <div class="tags-div">
          <div class="tag-div" v-for="item in type_names" :key="item.name">
            <div class="tag-type-div" v-if="info.tags[item.type]">{{ item.name }}</div>
            <div class="tags">
              <waku-tag v-for="tag in info.tags[item.type]" :key="tag.tag_id" :tag="tag"></waku-tag>
            </div>
          </div>
        </div>
        <div style="display: flex;flex-direction: row;gap: 20px; margin: 20px 0;">
          <waku-link class="source-div" @click="goto(info.post.source, true, false)">{{ 'Source: ' + info.post.source }}</waku-link>
          <waku-link class="uploader-div" @click="goto(`/user/${info.post.account_id}`, true)">{{ 'Uploader: ' + info.post.account_id }}</waku-link>
        </div>
        <div style="display: flex;flex-direction: row;gap: 20px">
          <div class="rect-div">{{ info.post.imgs[0].width + 'x' + info.post.imgs[0].height}}</div>
          <div class="date-div">{{ info.post.date }}</div>
          <div class="score-div">
            {{ info.post.score }}
            <div style="display: inline-block;height: 14px;vertical-align: bottom">
              <svg style="width: 14px;height: 14px" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" fill="CurrentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 5.72c-2.624-4.517-10-3.198-10 2.461 0 3.725 4.345 7.727 9.303 12.54.194.189.446.283.697.283s.503-.094.697-.283c4.977-4.831 9.303-8.814 9.303-12.54 0-5.678-7.396-6.944-10-2.461z" fill-rule="nonzero"/></svg>
            </div>
          </div>
        </div>
        <div style="margin: 20px 0; height: 2px;background-color: #AAAAAA"></div>
        <div style="display: flex;flex-direction: row;margin: 20px 0;gap: 20px">
          <waku-avatar :src="store.state.user.avatar_url" :size="40" style="margin: auto 0"></waku-avatar>
          <waku-input style="background-color: rgba(0, 0, 0, 0.02);width: 100%" label="发表评论">
            <template v-slot:before>
              <waku-deletable-item v-if="info.currentReply !== undefined" @delete="onDelete" style="height: 100%;font-size: 12px">
                {{ '回复给:' + info.currentReply.username }}
              </waku-deletable-item>
              <div v-if="info.currentReply !== undefined" style="height: 60%;width: 1px;margin: auto 5px;background-color: rgba(0 ,0 ,0 ,0.2);"></div>
            </template>
          </waku-input>
          <waku-button style="width: 100px;text-align: center" :enable="true">发送</waku-button>
        </div>
        <div class="comments-div">
          <waku-comment v-for="comment in info.comments" :key="comment.comment_id" :comment="comment" @reply="onReply"></waku-comment>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, watch} from 'vue'
import {getImageByID, goto, comment, postDetail, tag, getComments} from "@/assets/js/api";
import WakuStaticPost from "@/components/WakuStaticPost.vue";
import WakuTag from "@/components/WakuTag.vue"
import WakuButton from "@/components/WakuButton.vue"
import WakuInput from "@/components/WakuInput.vue";
import WakuAvatar from "@/components/WakuAvatar.vue";
import store from "@/store"
import WakuComment from "@/components/WakuComment.vue";
import WakuDeletableItem from "@/components/WakuDeletableItem.vue";
import WakuLink from "@/components/WakuLink.vue";
// eslint-disable-next-line no-undef
const props = defineProps<{
  id : string
}>()

const info = reactive<{
  post : postDetail
  tags : tag[][]
  comments : comment[]
  currentReply ?: comment
}>({
  post : new postDetail(),
  tags : [],
  comments: [],
  currentReply : undefined
})

const type_names = [
  { type: 1, name: '画师' },
  { type: 3, name: '作品' },
  { type: 4, name: '角色' },
  { type: 0, name: '标签' },
  { type: 5, name: '信息' }
]

const getTags = () => {
  info.tags = []
  // 按照tag的type分类
  for (const tag of info.post.tags) {
    if (info.tags[tag.type] === undefined) {
      info.tags[tag.type] = []
    }
    info.tags[tag.type].push(tag)
  }
}

const updateImage = (id : string) => {
  getImageByID(id).then((res) => {
    info.post = res
    updateContent()
    getTags()
    console.log(info.post)
  })
}

const updateContent = () => {
  // <http://www.baidu.com> -> <a href="http://www.baidu.com">http://www.baidu.com</a> 或https
  const reg2 = /<http(s?):\/\/(.*?)>/g
  info.post.content = info.post.content.replace(reg2, '<a class="content-link" style="color: #0077FF; text-decoration: none" href="http$1://$2">http$1://$2</a>')
  // 把info.post.content中形如 "string":[link] 的字符串替换为 <a href="link">string</a>
  // "string":[link] -> <a href="link">string</a>
  const reg1 = /"(.*?)":\[(.*?)\]/g
  info.post.content = info.post.content.replace(reg1, '<a class="content-link" style="color: #0077FF; text-decoration: none" href="$2">$1</a>')
}

watch(
  () => props.id,
  async (val, oldVal) => {
    updateImage(val)
    info.comments = await getComments(props.id, 1)
  },
  {
    immediate: true
  }
)

// const getComments = () => {
//   let out = []
//   let fa = new comment()
//   let fa2 = new comment()
//   let child = new comment()
//   fa.replies.push(child)
//   out.push(fa)
//   out.push(fa2)
//   return out
// }

const onReply = (comment : comment) => {
  console.log(comment)
  info.currentReply = comment
}

const onDelete = () => {
  info.currentReply = undefined
}
</script>

<style scoped>
.information-div {
  width: 700px;
  margin: auto;
  text-align: left;
}
.post-div {
  border-radius: 0;
  cursor: zoom-in;
}
.like-div {
  height: 40px;
  text-align: right;
  margin: 20px 0;
}
.title-div {
  font-size: 24px;
  margin: 20px 0;
  font-weight: 800;
}
.content-div {
  white-space: pre-wrap;
  margin: 20px 0;
}
.tags-div {
  display: inline-block;
}
.tag-div {
  /* width: 200px; */
  display: inline-block;
  font-weight: 600;
  font-size: 16px;
  color: rgba(0, 0, 0, 1.0);
  line-height: 22px;
  margin: 10px 0;
}
.rect-div,.date-div,.score-div, .source-div, .uploader-div {
  color: rgba(0, 0, 0, 0.4);
  font-size: 12px;
  /*margin: 20px 0;*/
}
/* .source-div {
  color: rgba(0, 0, 0, 0.4);
  font-size: 12px;
  margin: 20px 0;
} */
.comments-div {
  margin: 20px 0;
}
svg {
  width: 20px;
  height: 20px;
}
</style>
