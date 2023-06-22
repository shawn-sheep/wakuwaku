import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import EnterView from '../views/EnterView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import LoginView from '../views/LoginView.vue'
import MainView from '../views/MainView.vue'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import PostView from '../views/PostView.vue'
import SearchView from '../views/SearchView.vue'
import UserView from '../views/UserView.vue'
import TagsView from '../views/TagsView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/',
    name: 'welcome',
    component: WelcomeView,
    redirect: '/enter',
    children: [
      {
        path: '/login',
        name: 'login',
        component: LoginView
      },
      {
        path: '/enter',
        name: 'enter',
        component: EnterView
      },
      {
        path: '/register',
        name: 'register',
        component: RegisterView
      }
    ]
  },
  {
    path: '/main',
    name: 'main',
    component: MainView,
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'home',
        component: HomeView
      },
      {
        path: '/post/:id',
        name: 'post',
        props: true,
        component: PostView
      },
      {
        path: '/search',
        name: 'search',
        props: true,
        component: SearchView
      },
      {
        path: '/user/:userId',
        name: 'user',
        props: true,
        component: UserView
      },
      {
        path: '/tags',
        name: 'tags',
        component: TagsView
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
