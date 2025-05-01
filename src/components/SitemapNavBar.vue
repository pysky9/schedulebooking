<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container">
      <a class="navbar-brand" id="logo">吉時約 Schedule Booking</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/sitemap" active-class="active">
              <i class="bi bi-map"></i> 網站導覽
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/calendar" active-class="active">
              <i class="bi bi-calendar-check"></i> 預約行事曆
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/orders" active-class="active">
              <i class="bi bi-cart"></i> 訂單管理
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/settings" active-class="active">
              <i class="bi bi-gear"></i> 商家設定
            </router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link logout-link" @click="$emit('logout')">
              <i class="bi bi-box-arrow-right"></i> 登出
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'SitemapNavBar',
  emits: ['logout']
}
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: "Microsoft Jhenghei";
  font-weight: 500;
  padding: 12px 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.navbar-brand {
  font-family: "Microsoft Jhenghei";
  font-weight: 900;
  font-size: 28px;
  color: #3498db;
  transition: color 0.3s ease;
}

.navbar-brand:hover {
  color: #2980b9;
}

.navbar-nav {
  align-items: center;
}

.nav-item {
  margin: 0 5px;
  position: relative;
}

.nav-link {
  color: #555;
  font-size: 18px;
  padding: 8px 15px;
  border-radius: 5px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-link:hover, .nav-link.active {
  color: #3498db;
  background-color: rgba(52, 152, 219, 0.1);
}

.logout-link {
  color: #e74c3c;
  cursor: pointer;
}

.logout-link:hover {
  color: #c0392b;
  background-color: rgba(231, 76, 60, 0.1);
}

/* 響應式設計 */
@media (max-width: 992px) {
  .navbar-nav {
    margin-top: 15px;
  }
  
  .nav-item {
    margin: 5px 0;
  }
}
</style>
