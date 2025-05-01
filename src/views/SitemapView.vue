<template>
  <div>
    <sitemap-nav-bar @logout="handleLogout" />
    <sitemap-content @redirect-to-setting="redirectToSetting" />
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import SitemapNavBar from '@/components/SitemapNavBar.vue';
import SitemapContent from '@/components/SitemapContent.vue';
// 導入 CSS 樣式

export default {
  name: 'SitemapView',
  components: {
    SitemapNavBar,
    SitemapContent
  },
  setup() {
    const router = useRouter();
    
    const redirectToSetting = () => {
      router.push('/settings');
    };
    
    const handleLogout = () => {
      // 模擬登出功能
      console.log('用戶登出');
      // 將用戶導向到登入頁面
      router.push('/login');
    };
    
    return {
      redirectToSetting,
      handleLogout
    };
  }
}
</script>

<style scoped>
body {
  background-color: #f7f1f0;
}

li {
  margin-bottom: 0.5rem;
}

a {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s;
}

a:hover {
  color: #2980b9;
  text-decoration: underline;
}

#redirect-store-setting {
  color: #3498db;
  cursor: pointer;
}

#redirect-store-setting:hover {
  text-decoration: underline;
}

.about-line, .about-time-setting {
  margin-bottom: 1.5rem;
}
</style>
