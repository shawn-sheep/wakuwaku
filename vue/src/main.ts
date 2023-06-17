import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import lazyload from "@/plugins/lazyload";
import '@/assets/font/Inter Web/inter.css'

const app = createApp(App)
    .use(store)
    .use(router)
    .use(lazyload)
    .mount('#app')
