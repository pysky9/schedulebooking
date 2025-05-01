import axios from 'axios';

// 創建一個 axios 實例，設置基本 URL 和請求頭
const apiClient = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
});

// 請求攔截器 - 添加 CSRF Token
apiClient.interceptors.request.use(async (config) => {
  // 如果是修改數據的請求，需要 CSRF Token
  if (['post', 'put', 'delete', 'patch'].includes(config.method)) {
    try {
      // 獲取 CSRF Token
      const { data } = await axios.get('/api/csrf-token/');
      config.headers['X-CSRFToken'] = data.csrfToken;
    } catch (error) {
      console.error('獲取 CSRF Token 失敗:', error);
    }
  }
  return config;
});

// 用戶登錄
export const login = async (credentials) => {
  try {
    const response = await apiClient.post('/members/login/', credentials);
    return response.data;
  } catch (error) {
    console.error('登錄失敗:', error);
    throw error;
  }
};

// 用戶註冊
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/members/register/', userData);
    return response.data;
  } catch (error) {
    console.error('註冊失敗:', error);
    throw error;
  }
};

// 用戶登出
export const logout = async () => {
  try {
    const response = await apiClient.post('/members/logout/');
    return response.data;
  } catch (error) {
    console.error('登出失敗:', error);
    throw error;
  }
};

// 獲取用戶資料
export const getProfile = async () => {
  try {
    const response = await apiClient.get('/members/profile/');
    return response.data;
  } catch (error) {
    console.error('獲取用戶資料失敗:', error);
    throw error;
  }
};

// 更新用戶資料
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.post('/members/update_profile/', profileData);
    return response.data;
  } catch (error) {
    console.error('更新用戶資料失敗:', error);
    throw error;
  }
};

// 修改密碼
export const changePassword = async (passwordData) => {
  try {
    const response = await apiClient.post('/members/change_password/', passwordData);
    return response.data;
  } catch (error) {
    console.error('修改密碼失敗:', error);
    throw error;
  }
};

// 檢查認證狀態
export const checkAuth = async () => {
  try {
    const response = await apiClient.get('/members/check_auth/');
    return response.data;
  } catch (error) {
    console.error('檢查認證狀態失敗:', error);
    return { success: false, authenticated: false };
  }
};
