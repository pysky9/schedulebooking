import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 引入全局樣式
import './assets/main.css'

// 創建 Vue 應用實例
const app = createApp(App)

// 使用 Pinia 進行狀態管理
app.use(createPinia())

// 使用 Vue Router 進行路由管理
app.use(router)

// 掛載到 DOM
app.mount('#app')
