import { createStore } from 'vuex'
import {tag} from "@/assets/js/api";

export default createStore({
  state: {
    user: {
      account: '',
      username: 'Lierick',
      avatar: require('@/assets/img/user_avatar.jpg')
    },
    recommend: [
      {
        id: '1',
        src: require('@/assets/img/flotsam_77764886.jpg'),
        description: 'flotsam',
        tags: ['tag1', 'tag2'],
        width: 2088,
        height: 1488
      },
      {
        id: '2',
        src: require('@/assets/img/まとめ１２_81089162_p1.jpg'),
        description: 'まとめ１２',
        tags: ['tag2', 'tag3'],
        width: 900,
        height: 588
      },
      {
        id: '3',
        src: require('@/assets/img/エスニックJKモーニング_85918824.jpg'),
        description: 'エスニックJKモーニング',
        tags: ['tag3', 'tag4'],
        width: 2021,
        height: 1464
      },
      {
        id: '4',
        src: require('@/assets/img/夢見るフラミンゴ_86261533.jpg'),
        description: '夢見るフラミンゴ',
        tags: ['tag1', 'tag2','tag3'],
        width: 2652,
        height: 2512
      },
      {
        id: '5',
        src: require('@/assets/img/水族館_83088427_p1.jpg'),
        description: '水族館',
        tags: ['tag4', 'tag5', 'tag6'],
        width: 4000,
        height: 2267
      },
      {
        id: '6',
        src: require('@/assets/img/💙_106009822.jpg'),
        description: '💙',
        tags: ['tag1'],
        width: 2572,
        height: 4134
      }
    ],
    isDisplayImage: false,
    displayImage: {
      id: '',
      src: '',
      description: '',
      tags: [new tag()],
      width: 900,
      height: 588
    }
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
