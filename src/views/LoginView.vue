<template>
  <div class="login-container">
    <div class="login-form">
      <h2 class="text-center mb-4">登入/註冊</h2>
      
      <ul class="nav nav-tabs mb-4" id="loginTabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">
            登入
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'signup' }" @click="activeTab = 'signup'">
            註冊
          </button>
        </li>
      </ul>
      
      <div class="tab-content">
        <!-- 登入表單 -->
        <div v-if="activeTab === 'login'">
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="loginEmail" class="form-label">電子郵件</label>
              <input type="email" class="form-control" id="loginEmail" v-model="loginForm.email" required>
            </div>
            <div class="mb-3">
              <label for="loginPassword" class="form-label">密碼</label>
              <input type="password" class="form-control" id="loginPassword" v-model="loginForm.password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100 mt-3">登入</button>
          </form>
        </div>
        
        <!-- 註冊表單 -->
        <div v-if="activeTab === 'signup'">
          <form @submit.prevent="handleSignup">
            <div class="mb-3">
              <label for="signupEmail" class="form-label">電子郵件</label>
              <input type="email" class="form-control" id="signupEmail" v-model="signupForm.email" required>
            </div>
            <div class="mb-3">
              <label for="signupPassword" class="form-label">密碼</label>
              <input type="password" class="form-control" id="signupPassword" v-model="signupForm.password" required>
            </div>
            <div class="mb-3">
              <label for="signupConfirmPassword" class="form-label">確認密碼</label>
              <input type="password" class="form-control" id="signupConfirmPassword" v-model="signupForm.confirmPassword" required>
            </div>
            <button type="submit" class="btn btn-primary w-100 mt-3">註冊</button>
          </form>
        </div>
      </div>
      
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login, signup } from '../api/auth';

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter();
    const activeTab = ref('login');
    const errorMessage = ref('');
    
    const loginForm = ref({
      email: '',
      password: ''
    });
    
    const signupForm = ref({
      email: '',
      password: '',
      confirmPassword: ''
    });
    
    const handleLogin = async () => {
      try {
        errorMessage.value = '';
        const response = await login(loginForm.value);
        if (response.success) {
          // 登入成功，導航到日曆頁面
          router.push('/calendar');
        } else {
          errorMessage.value = response.message || '登入失敗，請檢查您的憑證';
        }
      } catch (error) {
        errorMessage.value = '登入過程中發生錯誤，請稍後再試';
        console.error('登入錯誤:', error);
      }
    };
    
    const handleSignup = async () => {
      try {
        errorMessage.value = '';
        
        // 檢查密碼是否匹配
        if (signupForm.value.password !== signupForm.value.confirmPassword) {
          errorMessage.value = '密碼不匹配';
          return;
        }
        
        const response = await signup({
          email: signupForm.value.email,
          password: signupForm.value.password
        });
        
        if (response.success) {
          // 註冊成功，切換到登入標籤
          activeTab.value = 'login';
          loginForm.value.email = signupForm.value.email;
          loginForm.value.password = '';
          // 清空註冊表單
          signupForm.value = {
            email: '',
            password: '',
            confirmPassword: ''
          };
        } else {
          errorMessage.value = response.message || '註冊失敗，請稍後再試';
        }
      } catch (error) {
        errorMessage.value = '註冊過程中發生錯誤，請稍後再試';
        console.error('註冊錯誤:', error);
      }
    };
    
    return {
      activeTab,
      loginForm,
      signupForm,
      errorMessage,
      handleLogin,
      handleSignup
    };
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--secondary-color);
}

.login-form {
  width: 100%;
  max-width: 450px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.nav-tabs .nav-link.active {
  font-weight: bold;
  color: var(--primary-color);
}
</style>
