<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">吉時約 Schedule Booking</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/sitemap" class="nav-link">網站導覽</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/calendar" class="nav-link">預約行事曆</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/orders" class="nav-link">訂單管理</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/settings" class="nav-link">商家設定</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="logout">登出</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';

export default {
  name: 'NavBar',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    
    const logout = async () => {
      const result = await authStore.logoutUser();
      if (result.success) {
        router.push('/login');
      }
    };
    
    return {
      logout
    };
  }
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.navbar-brand {
  font-weight: bold;
  color: var(--primary-color);
}

.nav-link {
  cursor: pointer;
  transition: color 0.3s;
}

.nav-link:hover {
  color: var(--primary-color) !important;
}
</style>
