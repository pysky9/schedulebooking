<template>
  <div class="container" id="site-map">
    <!-- 歡迎卡片 -->
    <div class="welcome-card">
      <div class="card welcome-message">
        <div class="card-body">
          <h5 class="welcome-title">
            <i class="bi bi-info-circle-fill me-2"></i>
            新手會員請前往 "<span id="redirect-store-setting" @click="$emit('redirect-to-setting')">商家設定</span>" 完成相關設定，謝謝。
          </h5>
        </div>
      </div>
    </div>
    
    <!-- 卡片容器 -->
    <div class="cards-container">
      <!-- LINE官方帳號卡片 -->
      <div class="card feature-card line-card">
        <div class="card-header">
          <h6 id="link-to-line">
            <i class="bi bi-line me-2"></i>
            連動LINE官方帳號
          </h6>
        </div>
        <div class="card-body">
          <ol>
            <li>請到LINE Develop註冊帳號(<a href="https://developers.line.biz/zh-hant/" target="_blank">官網</a>)</li>
            <li>申請LINE login Channel 以及 LIFF</li>
            <li>取得LIFF連結後，新增到官方帳號的圖文選單</li>
          </ol>
        </div>
      </div>

      <!-- 時段設定卡片 -->
      <div class="card feature-card time-card">
        <div class="card-header">
          <h6 id="store-time-setting">
            <i class="bi bi-calendar-check me-2"></i>
            時段設定
          </h6>
        </div>
        <div class="card-body">
          <ul>
            <li>完成所有必填欄位</li>
            <li>預約時段日期設定勿重疊</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SitemapContent',
  emits: ['redirect-to-setting']
}
</script>

<style scoped>
#site-map {
  font-family: "Microsoft Jhenghei";
  font-weight: 300;
  margin-top: 100px;
  padding: 0 20px;
}

/* 歡迎卡片樣式 */
.welcome-card {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.welcome-message {
  width: 100%;
  max-width: 800px;
  background-color: #e3f2fd;
  border-left: 5px solid #2196f3;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.welcome-message:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-3px);
}

.welcome-title {
  color: #0d47a1;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
}

/* 卡片容器樣式 */
.cards-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
}

/* 功能卡片共用樣式 */
.feature-card {
  width: 100%;
  max-width: 380px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.feature-card:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.feature-card .card-header {
  padding: 15px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.feature-card .card-body {
  padding: 20px;
}

/* LINE卡片特定樣式 */
.line-card {
  background-color: #f8f9fa;
  border-top: 5px solid #00c300;
}

.line-card .card-header {
  background-color: #00c300;
  color: white;
}

.line-card h6 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

/* 時段設定卡片特定樣式 */
.time-card {
  background-color: #f8f9fa;
  border-top: 5px solid #ff9800;
}

.time-card .card-header {
  background-color: #ff9800;
  color: white;
}

.time-card h6 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

/* 列表樣式 */
ol, ul {
  padding-left: 25px;
  margin-bottom: 0;
}

li {
  margin-bottom: 10px;
  line-height: 1.5;
}

li:last-child {
  margin-bottom: 0;
}

/* 連結樣式 */
a {
  color: #0d6efd;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

a:hover {
  color: #0a58ca;
  text-decoration: underline;
}

/* 商家設定連結樣式 */
#redirect-store-setting {
  color: #0d6efd;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s;
}

#redirect-store-setting:hover {
  color: #0a58ca;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .cards-container {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-card {
    max-width: 100%;
  }
}
</style>
