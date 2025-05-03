<template>
  <div>
    <login-header @redirect-home="redirectToHome" />
    <auth-form 
      :is-login="isLogin" 
      :is-loading="isLoading" 
      :error-message="errorMessage" 
      :success-message="successMessage" 
      @toggle-mode="toggleLoginSignup" 
      @submit-form="submitForm"
      @update:username="val => signupForm.username = val"
      @update:email="val => isLogin ? loginForm.email = val : signupForm.email = val"
      @update:password="val => isLogin ? loginForm.password = val : signupForm.password = val"
    />
    <login-footer />
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import LoginHeader from '@/components/LoginHeader.vue';
import AuthForm from '@/components/AuthForm.vue';
import LoginFooter from '@/components/LoginFooter.vue';
import { login, register } from '@/api/auth';

export default {
  name: 'LoginView',
  components: {
    LoginHeader,
    AuthForm,
    LoginFooter
  },
  setup() {
    const router = useRouter();
    
    // 響應式狀態
    const isLogin = ref(true);
    const isLoading = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');
    
    // 表單數據
    const loginForm = reactive({
      email: '',
      password: ''
    });
    
    const signupForm = reactive({
      username: '',
      email: '',
      password: ''
    });
    
    // 方法
    const redirectToHome = () => {
      router.push('/');
    };
    
    const toggleLoginSignup = () => {
      isLogin.value = !isLogin.value;
      errorMessage.value = '';
      successMessage.value = '';
    };
    
    const handleLogin = async () => {
      if (!loginForm.email || !loginForm.password) {
        errorMessage.value = '請填寫所有欄位';
        return;
      }
      
      isLoading.value = true;
      errorMessage.value = '';
      
      try {
        // 調用實際的登入 API
        const response = await login({
          email: loginForm.email,
          password: loginForm.password
        });
        
        console.log('登入響應:', response);
        
        if (response.success) {
          // 登入成功，導航到網站地圖頁面
          router.push('/sitemap');
        } else {
          // 登入失敗，顯示錯誤訊息
          errorMessage.value = response.message || '登入失敗';
        }
      } catch (error) {
        console.error('登入錯誤:', error);
        errorMessage.value = error.response?.data?.message || '登入失敗，請稍後再試';
      } finally {
        isLoading.value = false;
      }
    };
    
    const handleSignup = async () => {
      if (!signupForm.username || !signupForm.email || !signupForm.password) {
        errorMessage.value = '請填寫所有欄位';
        return;
      }
      
      isLoading.value = true;
      errorMessage.value = '';
      
      try {
        // 調用實際的註冊 API
        const response = await register({
          username: signupForm.username,
          email: signupForm.email,
          password: signupForm.password
        });
        
        console.log('註冊響應:', response);
        
        if (response.success) {
          // 註冊成功，顯示成功訊息並切換到登入
          successMessage.value = '註冊成功！請登入';
          isLogin.value = true;
          
          // 清空表單
          signupForm.username = '';
          signupForm.email = '';
          signupForm.password = '';
        } else {
          // 註冊失敗，顯示錯誤訊息
          errorMessage.value = response.message || '註冊失敗';
        }
      } catch (error) {
        console.error('註冊錯誤:', error);
        errorMessage.value = error.response?.data?.message || '註冊失敗，請稍後再試';
      } finally {
        isLoading.value = false;
      }
    };
    
    const submitForm = () => {
      if (isLogin.value) {
        handleLogin();
      } else {
        handleSignup();
      }
    };
    
    return {
      isLogin,
      isLoading,
      errorMessage,
      successMessage,
      loginForm,
      signupForm,
      redirectToHome,
      toggleLoginSignup,
      submitForm
    };
  }
}
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  background-color: #C3A6A0;
  font-family: "Microsoft Jhenghei";
}
</style>
