<template>
  <div class="auth-container">
    <div class="card">
      <div class="webName">吉時約</div>
      <div class="webName">Schedule Booking</div>
      <div class="formName">{{ isLogin ? '商家登入' : '商家註冊' }}</div>
      
      <form class="form-content">
        <div class="form-group" v-if="!isLogin">
          <label for="inputUsername" class="form-label">Username</label>
          <input type="text" class="form-control username" id="inputUsername" v-model="localFormData.username">
        </div>
        <div class="form-group">
          <label for="inputEmail" class="form-label">Email</label>
          <input type="email" class="form-control email" id="inputEmail" 
                 placeholder="ex. xxx@ccc.com" v-model="localFormData.email">
        </div>
        <div class="form-group">
          <label for="inputPassword" class="form-label">Password</label>
          <input type="password" class="form-control password" id="inputPassword" 
                 placeholder="6碼含英文(1碼大寫),數字,特殊符號" 
                 v-model="localFormData.password">
        </div>
      </form>
      
      <div id="buttonContainer">
        <button class="btn btn-primary" @click="submitForm" v-if="!isLoading">
          {{ isLogin ? 'Login' : 'Sign up' }}
        </button>
        <button class="btn btn-primary" type="button" disabled v-if="isLoading">
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          {{ isLogin ? 'Login' : 'Sign up' }}
        </button>
      </div>
      
      <div class="userStatus" @click="toggleMode">
        {{ isLogin ? '還沒有帳戶?點此註冊' : '已經有帳戶?點此登入' }}
      </div>
      
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
      
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthForm',
  props: {
    isLogin: {
      type: Boolean,
      required: true
    },
    isLoading: {
      type: Boolean,
      required: true
    },
    errorMessage: {
      type: String,
      default: ''
    },
    successMessage: {
      type: String,
      default: ''
    }
  },
  emits: ['toggle-mode', 'submit-form', 'update:username', 'update:email', 'update:password'],
  data() {
    return {
      localFormData: {
        username: '',
        email: '',
        password: ''
      }
    };
  },
  watch: {
    // 監聽表單數據變化並向父組件發送更新
    'localFormData.username'(val) {
      if (!this.isLogin) this.$emit('update:username', val);
    },
    'localFormData.email'(val) {
      this.$emit('update:email', val);
    },
    'localFormData.password'(val) {
      this.$emit('update:password', val);
    }
  },
  methods: {
    toggleMode() {
      this.$emit('toggle-mode');
    },
    submitForm() {
      this.$emit('submit-form');
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.card {
  background-color: white;
  border-radius: 15px;
  width: 400px;
  padding: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
}

.webName {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 800;
  font-size: 30px;
  text-align: center;
  padding-top: 5px;
  margin: 0;
}

.formName {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 400;
  font-size: 20px;
  text-align: center;
  padding-top: 5px;
  margin-bottom: 20px;
}

.form-content {
  width: 100%;
}

.form-group {
  margin-bottom: 10px;
  text-align: left;
}

.form-label {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 500;
  font-size: 15px;
  display: block;
  margin-bottom: 5px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

#buttonContainer {
  text-align: center;
  margin-top: 15px;
  display: flex;
  justify-content: center;
}

.btn-primary {
  padding: 0.5rem 2rem;
  background-color: #007bff;
  border: none;
  color: white;
  font-weight: 500;
}

.userStatus {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  margin-top: 10px;
  text-align: center;
  color: #3498db;
}

.userStatus:hover {
  text-decoration: underline;
}

.alert {
  margin-top: 1.5rem;
  text-align: center;
}

/* 移除靜態顯示/隱藏邏輯，改為使用 Vue 的條件渲染 */
</style>
