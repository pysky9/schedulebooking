<template>
  <div>
    <sitemap-nav-bar @logout="handleLogout" />
    
    <div class="container mt-3">
    
    <div class="setting-tabs mb-4">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'profile' }" @click="activeTab = 'profile'">
            基本資料
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'service' }" @click="activeTab = 'service'">
            服務設定
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'time' }" @click="activeTab = 'time'">
            時間設定
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'line' }" @click="activeTab = 'line'">
            LINE 設定
          </button>
        </li>
      </ul>
    </div>
    
    <div class="tab-content">
      <!-- 基本資料 -->
      <div v-if="activeTab === 'profile'" class="profile-settings">
        <form @submit.prevent="saveProfile">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">商家基本資料</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="storeName" class="form-label">商家名稱</label>
                <input type="text" class="form-control" id="storeName" v-model="profile.storeName" required>
              </div>
              <div class="mb-3">
                <label for="storePhone" class="form-label">聯絡電話</label>
                <input type="tel" class="form-control" id="storePhone" v-model="profile.storePhone" required>
              </div>
              <div class="mb-3">
                <label for="storeEmail" class="form-label">電子郵件</label>
                <input type="email" class="form-control" id="storeEmail" v-model="profile.storeEmail" required>
              </div>
              <div class="mb-3">
                <label for="storeAddress" class="form-label">商家地址</label>
                <input type="text" class="form-control" id="storeAddress" v-model="profile.storeAddress">
              </div>
              <div class="mb-3">
                <label for="storeDescription" class="form-label">商家簡介</label>
                <textarea class="form-control" id="storeDescription" rows="3" v-model="profile.storeDescription"></textarea>
              </div>
            </div>
          </div>
          
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">商家 Logo</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="storeLogo" class="form-label">上傳 Logo</label>
                <input type="file" class="form-control" id="storeLogo" @change="handleLogoUpload">
              </div>
              <div v-if="profile.logoUrl" class="text-center mt-3">
                <img :src="profile.logoUrl" alt="商家 Logo" class="img-thumbnail" style="max-height: 150px;">
              </div>
            </div>
          </div>
          
          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              儲存設定
            </button>
          </div>
        </form>
      </div>
      
      <!-- 服務設定 -->
      <div v-if="activeTab === 'service'" class="service-settings">
        <div class="card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">服務項目</h5>
            <button class="btn btn-sm btn-primary" @click="addNewService">新增服務</button>
          </div>
          <div class="card-body">
            <div v-if="services.length === 0" class="alert alert-info">
              尚未設定任何服務項目
            </div>
            
            <div v-else class="service-list">
              <div v-for="(service, index) in services" :key="index" class="service-item card mb-3">
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label :for="'serviceName' + index" class="form-label">服務名稱</label>
                        <input type="text" class="form-control" :id="'serviceName' + index" v-model="service.name" required>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label :for="'servicePrice' + index" class="form-label">服務價格 (NT$)</label>
                        <input type="number" class="form-control" :id="'servicePrice' + index" v-model="service.price" min="0" required>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label :for="'serviceDuration' + index" class="form-label">服務時長</label>
                        <div class="input-group">
                          <input type="number" class="form-control" :id="'serviceDuration' + index" v-model="service.duration" min="1" required>
                          <select class="form-select" v-model="service.durationUnit">
                            <option value="minute">分鐘</option>
                            <option value="hour">小時</option>
                          </select>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label :for="'serviceStatus' + index" class="form-label">狀態</label>
                        <select class="form-select" :id="'serviceStatus' + index" v-model="service.status">
                          <option value="active">啟用</option>
                          <option value="inactive">停用</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="mb-3">
                    <label :for="'serviceDescription' + index" class="form-label">服務說明</label>
                    <textarea class="form-control" :id="'serviceDescription' + index" rows="2" v-model="service.description"></textarea>
                  </div>
                  <div class="d-flex justify-content-end">
                    <button class="btn btn-danger btn-sm" @click="removeService(index)">刪除</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
          <button type="button" class="btn btn-primary" @click="saveServices" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            儲存設定
          </button>
        </div>
      </div>
      
      <!-- 時間設定 -->
      <div v-if="activeTab === 'time'" class="time-settings">
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">營業時間</h5>
          </div>
          <div class="card-body">
            <div v-for="(day, index) in businessHours" :key="day.dayOfWeek" class="mb-3">
              <div class="d-flex align-items-center mb-2">
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" :id="'day' + index" v-model="day.isOpen">
                  <label class="form-check-label" :for="'day' + index">{{ getDayName(day.dayOfWeek) }}</label>
                </div>
              </div>
              
              <div v-if="day.isOpen" class="time-slots">
                <div v-for="(timeSlot, slotIndex) in day.timeSlots" :key="slotIndex" class="row mb-2">
                  <div class="col-5">
                    <input type="time" class="form-control" v-model="timeSlot.start">
                  </div>
                  <div class="col-1 text-center">至</div>
                  <div class="col-5">
                    <input type="time" class="form-control" v-model="timeSlot.end">
                  </div>
                  <div class="col-1">
                    <button type="button" class="btn btn-outline-danger btn-sm" @click="removeTimeSlot(index, slotIndex)">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
                
                <button type="button" class="btn btn-outline-primary btn-sm mt-2" @click="addTimeSlot(index)">
                  新增時段
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">特殊日期</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <button type="button" class="btn btn-outline-primary" @click="addSpecialDate">新增特殊日期</button>
            </div>
            
            <div v-if="specialDates.length === 0" class="alert alert-info">
              尚未設定任何特殊日期
            </div>
            
            <div v-else class="special-dates-list">
              <div v-for="(specialDate, index) in specialDates" :key="index" class="card mb-3">
                <div class="card-body">
                  <div class="row mb-3">
                    <div class="col-md-4">
                      <label :for="'specialDate' + index" class="form-label">日期</label>
                      <input type="date" class="form-control" :id="'specialDate' + index" v-model="specialDate.date">
                    </div>
                    <div class="col-md-4">
                      <label :for="'specialDateType' + index" class="form-label">類型</label>
                      <select class="form-select" :id="'specialDateType' + index" v-model="specialDate.type">
                        <option value="closed">休息日</option>
                        <option value="custom">自訂時間</option>
                      </select>
                    </div>
                    <div class="col-md-4">
                      <label :for="'specialDateName' + index" class="form-label">說明</label>
                      <input type="text" class="form-control" :id="'specialDateName' + index" v-model="specialDate.name" placeholder="例如：國定假日">
                    </div>
                  </div>
                  
                  <div v-if="specialDate.type === 'custom'" class="time-slots">
                    <div v-for="(timeSlot, slotIndex) in specialDate.timeSlots" :key="slotIndex" class="row mb-2">
                      <div class="col-5">
                        <input type="time" class="form-control" v-model="timeSlot.start">
                      </div>
                      <div class="col-1 text-center">至</div>
                      <div class="col-5">
                        <input type="time" class="form-control" v-model="timeSlot.end">
                      </div>
                      <div class="col-1">
                        <button type="button" class="btn btn-outline-danger btn-sm" @click="removeSpecialDateTimeSlot(index, slotIndex)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                    
                    <button type="button" class="btn btn-outline-primary btn-sm mt-2" @click="addSpecialDateTimeSlot(index)">
                      新增時段
                    </button>
                  </div>
                  
                  <div class="d-flex justify-content-end mt-3">
                    <button class="btn btn-danger btn-sm" @click="removeSpecialDate(index)">刪除</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
          <button type="button" class="btn btn-primary" @click="saveTimeSettings" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            儲存設定
          </button>
        </div>
      </div>
      
      <!-- LINE 設定 -->
      <div v-if="activeTab === 'line'" class="line-settings">
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">LINE 官方帳號設定</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label for="lineChannelId" class="form-label">Channel ID</label>
              <input type="text" class="form-control" id="lineChannelId" v-model="lineSettings.channelId">
            </div>
            <div class="mb-3">
              <label for="lineChannelSecret" class="form-label">Channel Secret</label>
              <input type="password" class="form-control" id="lineChannelSecret" v-model="lineSettings.channelSecret">
            </div>
            <div class="mb-3">
              <label for="lineAccessToken" class="form-label">Channel Access Token</label>
              <input type="password" class="form-control" id="lineAccessToken" v-model="lineSettings.accessToken">
            </div>
            <div class="mb-3">
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" id="lineEnabled" v-model="lineSettings.enabled">
                <label class="form-check-label" for="lineEnabled">啟用 LINE 通知</label>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">通知設定</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="notifyNewOrder" v-model="lineSettings.notifications.newOrder">
                <label class="form-check-label" for="notifyNewOrder">新訂單通知</label>
              </div>
            </div>
            <div class="mb-3">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="notifyCancelOrder" v-model="lineSettings.notifications.cancelOrder">
                <label class="form-check-label" for="notifyCancelOrder">取消訂單通知</label>
              </div>
            </div>
            <div class="mb-3">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="notifyReminder" v-model="lineSettings.notifications.reminder">
                <label class="form-check-label" for="notifyReminder">預約提醒通知</label>
              </div>
            </div>
            <div class="mb-3">
              <label for="reminderTime" class="form-label">提前提醒時間</label>
              <div class="input-group">
                <input type="number" class="form-control" id="reminderTime" v-model="lineSettings.reminderTime" min="1">
                <select class="form-select" v-model="lineSettings.reminderUnit">
                  <option value="hour">小時</option>
                  <option value="day">天</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
          <button type="button" class="btn btn-primary" @click="saveLineSettings" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            儲存設定
          </button>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import SitemapNavBar from '@/components/SitemapNavBar.vue';

export default {
  name: 'SettingView',
  components: {
    SitemapNavBar
  },
  setup() {
    const router = useRouter();
    const activeTab = ref('profile');
    const saving = ref(false);
    
    // 處理登出
    const handleLogout = () => {
      console.log('用戶登出');
      router.push('/login');
    };
    
    // 基本資料
    const profile = ref({
      storeName: '',
      storePhone: '',
      storeEmail: '',
      storeAddress: '',
      storeDescription: '',
      logoUrl: ''
    });
    
    // 服務設定
    const services = ref([]);
    
    // 時間設定
    const businessHours = ref([
      { dayOfWeek: 0, isOpen: false, timeSlots: [{ start: '09:00', end: '18:00' }] }, // 週日
      { dayOfWeek: 1, isOpen: true, timeSlots: [{ start: '09:00', end: '18:00' }] },  // 週一
      { dayOfWeek: 2, isOpen: true, timeSlots: [{ start: '09:00', end: '18:00' }] },  // 週二
      { dayOfWeek: 3, isOpen: true, timeSlots: [{ start: '09:00', end: '18:00' }] },  // 週三
      { dayOfWeek: 4, isOpen: true, timeSlots: [{ start: '09:00', end: '18:00' }] },  // 週四
      { dayOfWeek: 5, isOpen: true, timeSlots: [{ start: '09:00', end: '18:00' }] },  // 週五
      { dayOfWeek: 6, isOpen: false, timeSlots: [{ start: '09:00', end: '18:00' }] }  // 週六
    ]);
    
    const specialDates = ref([]);
    
    // LINE 設定
    const lineSettings = ref({
      channelId: '',
      channelSecret: '',
      accessToken: '',
      enabled: false,
      notifications: {
        newOrder: true,
        cancelOrder: true,
        reminder: true
      },
      reminderTime: 1,
      reminderUnit: 'day'
    });
    
    // 獲取星期幾的名稱
    const getDayName = (dayOfWeek) => {
      const days = ['週日', '週一', '週二', '週三', '週四', '週五', '週六'];
      return days[dayOfWeek];
    };
    
    // 獲取商家資料
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/members/store_profile/');
        if (response.data.success) {
          profile.value = response.data.profile;
        }
      } catch (error) {
        console.error('獲取商家資料失敗:', error);
      }
    };
    
    // 獲取服務設定
    const fetchServices = async () => {
      try {
        const response = await axios.get('/api/members/services/');
        if (response.data.success) {
          services.value = response.data.services;
        }
      } catch (error) {
        console.error('獲取服務設定失敗:', error);
      }
    };
    
    // 獲取時間設定
    const fetchTimeSettings = async () => {
      try {
        const response = await axios.get('/api/members/time_settings/');
        if (response.data.success) {
          businessHours.value = response.data.businessHours;
          specialDates.value = response.data.specialDates;
        }
      } catch (error) {
        console.error('獲取時間設定失敗:', error);
      }
    };
    
    // 獲取 LINE 設定
    const fetchLineSettings = async () => {
      try {
        const response = await axios.get('/api/members/line_settings/');
        if (response.data.success) {
          lineSettings.value = response.data.lineSettings;
        }
      } catch (error) {
        console.error('獲取 LINE 設定失敗:', error);
      }
    };
    
    // 上傳 Logo
    const handleLogoUpload = (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      // 這裡可以添加文件類型和大小的驗證
      
      // 創建一個臨時的 URL 來顯示預覽
      profile.value.logoUrl = URL.createObjectURL(file);
      
      // 實際上傳邏輯將在 saveProfile 中處理
    };
    
    // 保存商家資料
    const saveProfile = async () => {
      saving.value = true;
      try {
        const response = await axios.post('/api/members/save_profile/', profile.value);
        if (response.data.success) {
          alert('商家資料已保存');
        } else {
          alert('保存失敗: ' + response.data.message);
        }
      } catch (error) {
        console.error('保存商家資料失敗:', error);
        alert('保存失敗，請稍後再試');
      } finally {
        saving.value = false;
      }
    };
    
    // 添加新服務
    const addNewService = () => {
      services.value.push({
        name: '',
        price: 0,
        duration: 60,
        durationUnit: 'minute',
        description: '',
        status: 'active'
      });
    };
    
    // 移除服務
    const removeService = (index) => {
      if (confirm('確定要刪除此服務嗎？')) {
        services.value.splice(index, 1);
      }
    };
    
    // 保存服務設定
    const saveServices = async () => {
      saving.value = true;
      try {
        const response = await axios.post('/api/members/save_services/', { services: services.value });
        if (response.data.success) {
          alert('服務設定已保存');
        } else {
          alert('保存失敗: ' + response.data.message);
        }
      } catch (error) {
        console.error('保存服務設定失敗:', error);
        alert('保存失敗，請稍後再試');
      } finally {
        saving.value = false;
      }
    };
    
    // 添加時間段
    const addTimeSlot = (dayIndex) => {
      businessHours.value[dayIndex].timeSlots.push({ start: '09:00', end: '18:00' });
    };
    
    // 移除時間段
    const removeTimeSlot = (dayIndex, slotIndex) => {
      if (businessHours.value[dayIndex].timeSlots.length > 1) {
        businessHours.value[dayIndex].timeSlots.splice(slotIndex, 1);
      } else {
        alert('每個營業日至少需要一個時間段');
      }
    };
    
    // 添加特殊日期
    const addSpecialDate = () => {
      const today = new Date();
      const formattedDate = today.toISOString().split('T')[0];
      
      specialDates.value.push({
        date: formattedDate,
        type: 'closed',
        name: '',
        timeSlots: [{ start: '09:00', end: '18:00' }]
      });
    };
    
    // 移除特殊日期
    const removeSpecialDate = (index) => {
      if (confirm('確定要刪除此特殊日期嗎？')) {
        specialDates.value.splice(index, 1);
      }
    };
    
    // 添加特殊日期時間段
    const addSpecialDateTimeSlot = (dateIndex) => {
      specialDates.value[dateIndex].timeSlots.push({ start: '09:00', end: '18:00' });
    };
    
    // 移除特殊日期時間段
    const removeSpecialDateTimeSlot = (dateIndex, slotIndex) => {
      if (specialDates.value[dateIndex].timeSlots.length > 1) {
        specialDates.value[dateIndex].timeSlots.splice(slotIndex, 1);
      } else {
        alert('每個特殊日期至少需要一個時間段');
      }
    };
    
    // 保存時間設定
    const saveTimeSettings = async () => {
      saving.value = true;
      try {
        const response = await axios.post('/api/members/save_time_settings/', {
          businessHours: businessHours.value,
          specialDates: specialDates.value
        });
        if (response.data.success) {
          alert('時間設定已保存');
        } else {
          alert('保存失敗: ' + response.data.message);
        }
      } catch (error) {
        console.error('保存時間設定失敗:', error);
        alert('保存失敗，請稍後再試');
      } finally {
        saving.value = false;
      }
    };
    
    // 保存 LINE 設定
    const saveLineSettings = async () => {
      saving.value = true;
      try {
        const response = await axios.post('/api/members/save_line_settings/', lineSettings.value);
        if (response.data.success) {
          alert('LINE 設定已保存');
        } else {
          alert('保存失敗: ' + response.data.message);
        }
      } catch (error) {
        console.error('保存 LINE 設定失敗:', error);
        alert('保存失敗，請稍後再試');
      } finally {
        saving.value = false;
      }
    };
    
    onMounted(() => {
      fetchProfile();
      fetchServices();
      fetchTimeSettings();
      fetchLineSettings();
    });
    
    return {
      activeTab,
      saving,
      profile,
      services,
      businessHours,
      specialDates,
      lineSettings,
      getDayName,
      handleLogoUpload,
      saveProfile,
      addNewService,
      removeService,
      saveServices,
      addTimeSlot,
      removeTimeSlot,
      addSpecialDate,
      removeSpecialDate,
      addSpecialDateTimeSlot,
      removeSpecialDateTimeSlot,
      saveTimeSettings,
      saveLineSettings,
      handleLogout
    };
  }
}
</script>

<style scoped>
.setting-view {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: var(--primary-color);
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.card {
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.card-header {
  background-color: #f8f9fa;
}

.time-slots {
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.form-switch .form-check-input {
  width: 3em;
}
</style>
