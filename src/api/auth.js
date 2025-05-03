import axios from 'axios';

// 創建一個 axios 實例，設置基本 URL 和請求頭
const apiClient = axios.create({
  baseURL: '/members',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
});

// 請求攔截器 - 添加 CSRF Token 和 JWT Token
apiClient.interceptors.request.use(async (config) => {
  // 如果是修改數據的請求，需要 CSRF Token
  if (['post', 'put', 'delete', 'patch'].includes(config.method)) {
    try {
      // 獲取 CSRF Token
      const { data } = await axios.get('/csrf-token/');
      config.headers['X-CSRFToken'] = data.csrfToken;
    } catch (error) {
      console.error('獲取 CSRF Token 失敗:', error);
    }
  }
  
  // 添加 JWT Token 到 Authorization 頭
  const jwt_token = localStorage.getItem('jwt_token');
  if (jwt_token) {
    config.headers['Authorization'] = `Bearer ${jwt_token}`;
  }
  
  return config;
});

// 響應攔截器 - 處理 JWT 過期
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // 可能是 JWT 過期，清除本地存儲的用戶信息和 token
      localStorage.removeItem('user');
      localStorage.removeItem('jwt_token');
      
      // 如果需要，可以重定向到登入頁面
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// 用戶登錄
export const login = async (credentials) => {
  try {
    const response = await apiClient.post('/login/', credentials);
    
    // 存儲用戶信息和 JWT token 到本地存儲
    if (response.data.success) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      // 從 cookie 中獲取 JWT token 並存儲到 localStorage
      // 注意：這是為了在前端也能訪問到 token，因為 httpOnly cookie 無法通過 JS 訪問
      const cookies = document.cookie.split(';');
      const jwt_cookie = cookies.find(cookie => cookie.trim().startsWith('jwt_token='));
      if (jwt_cookie) {
        const jwt_token = jwt_cookie.split('=')[1];
        localStorage.setItem('jwt_token', jwt_token);
      }
    }
    
    return response.data;
  } catch (error) {
    console.error('登錄失敗:', error);
    throw error;
  }
};

// 用戶註冊
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/register/', userData);
    
    // 存儲用戶信息和 JWT token 到本地存儲
    if (response.data.success) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      // 從 cookie 中獲取 JWT token 並存儲到 localStorage
      const cookies = document.cookie.split(';');
      const jwt_cookie = cookies.find(cookie => cookie.trim().startsWith('jwt_token='));
      if (jwt_cookie) {
        const jwt_token = jwt_cookie.split('=')[1];
        localStorage.setItem('jwt_token', jwt_token);
      }
    }
    
    return response.data;
  } catch (error) {
    console.error('註冊失敗:', error);
    throw error;
  }
};

// 用戶登出
export const logout = async () => {
  try {
    const response = await apiClient.post('/logout/');
    
    // 清除本地存儲的用戶信息和 token
    localStorage.removeItem('user');
    localStorage.removeItem('jwt_token');
    
    return response.data;
  } catch (error) {
    console.error('登出失敗:', error);
    // 即使 API 調用失敗，也清除本地存儲
    localStorage.removeItem('user');
    localStorage.removeItem('jwt_token');
    throw error;
  }
};

// 獲取用戶資料
export const getProfile = async () => {
  try {
    const response = await apiClient.get('/profile/');
    
    // 更新本地存儲的用戶信息
    if (response.data.success) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  } catch (error) {
    console.error('獲取用戶資料失敗:', error);
    throw error;
  }
};

// 更新用戶資料
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.post('/update_profile/', profileData);
    
    // 更新本地存儲的用戶信息
    if (response.data.success) {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      localStorage.setItem('user', JSON.stringify({
        ...user,
        ...response.data.user
      }));
    }
    
    return response.data;
  } catch (error) {
    console.error('更新用戶資料失敗:', error);
    throw error;
  }
};

// 修改密碼
export const changePassword = async (passwordData) => {
  try {
    const response = await apiClient.post('/change_password/', passwordData);
    return response.data;
  } catch (error) {
    console.error('修改密碼失敗:', error);
    throw error;
  }
};

// 檢查認證狀態
export const checkAuth = async () => {
  try {
    const response = await apiClient.get('/check_auth/');
    
    // 如果已認證，更新本地存儲的用戶信息
    if (response.data.success && response.data.authenticated) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
    } else {
      // 如果未認證，清除本地存儲的用戶信息和 token
      localStorage.removeItem('user');
      localStorage.removeItem('jwt_token');
    }
    
    return response.data;
  } catch (error) {
    console.error('檢查認證狀態失敗:', error);
    // 清除本地存儲的用戶信息和 token
    localStorage.removeItem('user');
    localStorage.removeItem('jwt_token');
    return { success: false, authenticated: false };
  }
};

// 獲取當前用戶
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

// 判斷用戶是否已登入
export const isAuthenticated = () => {
  return !!localStorage.getItem('user');
};
