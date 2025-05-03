import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      // 將 API 請求代理到 Django 後端
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      // 將 members 路徑代理到 Django 後端
      '/members': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // 將 csrf-token 路徑代理到 Django 後端
      '/csrf-token': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
