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

// 創建訂單
export const createOrder = async (orderData) => {
  try {
    const response = await apiClient.post('/order/create_order/', orderData);
    return response.data;
  } catch (error) {
    console.error('創建訂單失敗:', error);
    throw error;
  }
};

// 獲取訂單列表
export const getOrders = async (role = 'consumer') => {
  try {
    const response = await apiClient.get(`/order/get_orders/?role=${role}`);
    return response.data;
  } catch (error) {
    console.error('獲取訂單列表失敗:', error);
    throw error;
  }
};

// 獲取訂單詳情
export const getOrderDetails = async (orderId) => {
  try {
    const response = await apiClient.get(`/order/get_order_details/${orderId}/`);
    return response.data;
  } catch (error) {
    console.error('獲取訂單詳情失敗:', error);
    throw error;
  }
};

// 更新訂單狀態
export const updateOrderStatus = async (orderId, status) => {
  try {
    const response = await apiClient.post('/order/update_order_status/', {
      order_id: orderId,
      status: status
    });
    return response.data;
  } catch (error) {
    console.error('更新訂單狀態失敗:', error);
    throw error;
  }
};

// 取消訂單
export const cancelOrder = async (orderId) => {
  try {
    const response = await apiClient.post('/order/cancel_order/', {
      order_id: orderId
    });
    return response.data;
  } catch (error) {
    console.error('取消訂單失敗:', error);
    throw error;
  }
};
