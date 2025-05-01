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

// 獲取預約時間列表
export const getAppointmentTimes = async () => {
  try {
    const response = await apiClient.get('/calendar/reservation_times/');
    return response.data;
  } catch (error) {
    console.error('獲取預約時間失敗:', error);
    throw error;
  }
};

// 獲取時間段設置
export const getTimePeriods = async () => {
  try {
    const response = await apiClient.get('/calendar/time_periods/');
    return response.data;
  } catch (error) {
    console.error('獲取時間段設置失敗:', error);
    throw error;
  }
};

// 保存時間段設置
export const saveTimePeriod = async (timePeriodData) => {
  try {
    const response = await apiClient.post('/calendar/time_periods/', timePeriodData);
    return response.data;
  } catch (error) {
    console.error('保存時間段設置失敗:', error);
    throw error;
  }
};

// 獲取時間價格設置
export const getTimePrices = async () => {
  try {
    const response = await apiClient.get('/calendar/time_prices/');
    return response.data;
  } catch (error) {
    console.error('獲取時間價格設置失敗:', error);
    throw error;
  }
};

// 保存時間價格設置
export const saveTimePrice = async (timePriceData) => {
  try {
    const response = await apiClient.post('/calendar/time_prices/', timePriceData);
    return response.data;
  } catch (error) {
    console.error('保存時間價格設置失敗:', error);
    throw error;
  }
};

// 獲取商家時間段
export const getMerchantTimeSlots = async () => {
  try {
    const response = await apiClient.get('/calendar/merchant_time_slots/');
    return response.data;
  } catch (error) {
    console.error('獲取商家時間段失敗:', error);
    throw error;
  }
};

// 更新商家時間段
export const updateMerchantTimeSlot = async (timeSlotData) => {
  try {
    const response = await apiClient.post('/calendar/merchant_time_slots/update/', timeSlotData);
    return response.data;
  } catch (error) {
    console.error('更新商家時間段失敗:', error);
    throw error;
  }
};

// 刪除商家時間段
export const deleteMerchantTimeSlot = async (timeSlotId) => {
  try {
    const response = await apiClient.post('/calendar/merchant_time_slots/delete/', { time_slot_id: timeSlotId });
    return response.data;
  } catch (error) {
    console.error('刪除商家時間段失敗:', error);
    throw error;
  }
};
