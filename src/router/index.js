import { createRouter, createWebHistory } from 'vue-router'
import CalendarView from '../views/CalendarView.vue'

const routes = [
  {
    path: '/',
    redirect: '/calendar'
  },
  {
    path: '/calendar',
    name: 'calendar',
    component: CalendarView
  },
  {
    path: '/orders',
    name: 'orders',
    // 使用懶加載來提高性能
    component: () => import('../views/OrderView.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../views/SettingView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/sitemap',
    name: 'sitemap',
    component: () => import('../views/SitemapView.vue')
  },
  // 404 頁面
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守衛 - 可用於驗證用戶是否已登錄
router.beforeEach((to, from, next) => {
  // 這裡可以添加身份驗證邏輯
  // 例如: 檢查是否已登錄，如果未登錄且訪問需要登錄的頁面，則重定向到登錄頁面
  next()
})

export default router
