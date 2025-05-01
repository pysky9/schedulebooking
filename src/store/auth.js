import { defineStore } from 'pinia';
import { login, logout, getCurrentUser } from '../api/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),
  
  getters: {
    // 獲取用戶信息
    currentUser: (state) => state.user,
    
    // 檢查用戶是否已登錄
    isLoggedIn: (state) => state.isAuthenticated,
    
    // 檢查是否正在加載
    isLoading: (state) => state.loading
  },
  
  actions: {
    // 設置加載狀態
    setLoading(status) {
      this.loading = status;
    },
    
    // 設置錯誤信息
    setError(error) {
      this.error = error;
    },
    
    // 設置用戶信息
    setUser(user) {
      this.user = user;
      this.isAuthenticated = !!user;
    },
    
    // 登錄
    async loginUser(credentials) {
      this.setLoading(true);
      this.setError(null);
      
      try {
        const response = await login(credentials);
        if (response.success) {
          this.setUser(response.user);
          return { success: true };
        } else {
          this.setError(response.message || '登入失敗');
          return { success: false, message: response.message };
        }
      } catch (error) {
        const message = error.response?.data?.message || '登入過程中發生錯誤';
        this.setError(message);
        return { success: false, message };
      } finally {
        this.setLoading(false);
      }
    },
    
    // 登出
    async logoutUser() {
      this.setLoading(true);
      this.setError(null);
      
      try {
        await logout();
        this.setUser(null);
        return { success: true };
      } catch (error) {
        const message = error.response?.data?.message || '登出過程中發生錯誤';
        this.setError(message);
        return { success: false, message };
      } finally {
        this.setLoading(false);
      }
    },
    
    // 獲取當前用戶信息
    async fetchCurrentUser() {
      this.setLoading(true);
      this.setError(null);
      
      try {
        const response = await getCurrentUser();
        if (response.success) {
          this.setUser(response.user);
        } else {
          this.setUser(null);
        }
        return { success: true };
      } catch (error) {
        this.setUser(null);
        const message = error.response?.data?.message || '獲取用戶信息失敗';
        this.setError(message);
        return { success: false, message };
      } finally {
        this.setLoading(false);
      }
    }
  }
});
