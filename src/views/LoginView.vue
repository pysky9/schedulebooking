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
    
    const handleLogin = () => {
      if (!loginForm.email || !loginForm.password) {
        errorMessage.value = '請填寫所有欄位';
        return;
      }
      
      isLoading.value = true;
      
      // 模擬 API 請求
      setTimeout(() => {
        console.log('登入', loginForm);
        isLoading.value = false;
        
        // 假設登入成功，導航到網站地圖頁面
        router.push('/sitemap');
      }, 1500);
    };
    
    const handleSignup = () => {
      if (!signupForm.username || !signupForm.email || !signupForm.password) {
        errorMessage.value = '請填寫所有欄位';
        return;
      }
      
      isLoading.value = true;
      
      // 模擬 API 請求
      setTimeout(() => {
        console.log('註冊', signupForm);
        isLoading.value = false;
        
        // 假設註冊成功，顯示成功訊息並切換到登入
        successMessage.value = '註冊成功！請登入';
        isLogin.value = true;
      }, 1500);
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
