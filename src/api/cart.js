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

// 創建預約
export const createBooking = async (bookingData) => {
  try {
    const response = await apiClient.post('/cart/booking/', bookingData);
    return response.data;
  } catch (error) {
    console.error('創建預約失敗:', error);
    throw error;
  }
};

// 添加項目到購物車
export const addToCart = async (bookingId, quantity = 1) => {
  try {
    const response = await apiClient.post('/cart/add_to_cart/', {
      booking_id: bookingId,
      quantity: quantity
    });
    return response.data;
  } catch (error) {
    console.error('添加到購物車失敗:', error);
    throw error;
  }
};

// 獲取購物車內容
export const getCart = async () => {
  try {
    const response = await apiClient.get('/cart/get_cart/');
    return response.data;
  } catch (error) {
    console.error('獲取購物車失敗:', error);
    throw error;
  }
};

// 更新購物車項目數量
export const updateCartItem = async (cartItemId, quantity) => {
  try {
    const response = await apiClient.post('/cart/update_cart_item/', {
      cart_item_id: cartItemId,
      quantity: quantity
    });
    return response.data;
  } catch (error) {
    console.error('更新購物車項目失敗:', error);
    throw error;
  }
};

// 從購物車中移除項目
export const removeCartItem = async (cartItemId) => {
  try {
    const response = await apiClient.post('/cart/remove_cart_item/', {
      cart_item_id: cartItemId
    });
    return response.data;
  } catch (error) {
    console.error('移除購物車項目失敗:', error);
    throw error;
  }
};

// 清空購物車
export const clearCart = async () => {
  try {
    const response = await apiClient.post('/cart/clear_cart/');
    return response.data;
  } catch (error) {
    console.error('清空購物車失敗:', error);
    throw error;
  }
};
