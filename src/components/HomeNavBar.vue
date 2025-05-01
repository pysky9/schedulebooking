<template>
  <nav class="navbar navbar-light bg-light" id="main-navbar">
    <div class="container-fluid">
      <a class="navbar-brand">吉時約 Schedule Booking</a>
      <div class="button-container">
        <button type="button" class="btn btn-outline-primary white-button" id="btn-literal" @click="$emit('redirect-login')">Let's Start</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'HomeNavBar',
  emits: ['redirect-login']
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  flex-wrap: wrap;
  font-weight: 500;
  padding-top: 5px;
  font-size: 20px;
  cursor: pointer;
  background-color: white !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-family: "Microsoft Jhenghei";
  font-weight: 900;
  padding-top: 5px;
  font-size: 30px;
}

.button-container {
  margin-left: auto; /* 使按鈕靠右顯示 */
  margin-right: 20px; /* 距離右邊的間距 */
}

#btn-literal {
  font-family: "Microsoft Jhenghei";
  font-size: 18px; /* 調整字體大小以符合圖片中的按鈕 */
}

.white-button {
  background-color: white; /* 白底 */
  color: #007bff; /* 藍色文字 */
  border: 1px solid #007bff; /* 藍框 */
  border-radius: 5px; /* 輕微圓角 */
  padding: 8px 20px;
  transition: all 0.2s ease;
}

.white-button:hover {
  background-color: #f8f9fa; /* 應該在應用中已經定義了這個顏色 */
}
</style>
