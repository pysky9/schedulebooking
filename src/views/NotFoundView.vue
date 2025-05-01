<template>
  <div class="not-found">
    <div class="container">
      <div class="error-content text-center">
        <h1>404</h1>
        <h2>頁面不存在</h2>
        <p>很抱歉，您要尋找的頁面不存在或已被移除。</p>
        <router-link to="/" class="btn btn-primary">返回首頁</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.error-content {
  max-width: 500px;
  margin: 0 auto;
}

h1 {
  font-size: 8rem;
  color: var(--primary-color);
  margin-bottom: 0;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 2rem;
  color: #6c757d;
}
</style>
