<template>
  <div>
    <sitemap-nav-bar @logout="handleLogout" />
    
    <div class="container mt-3">
      
      <div class="order-tabs mb-4">
        <ul class="nav nav-tabs">
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'current' }" @click="activeTab = 'current'">
              當前訂單
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'history' }" @click="activeTab = 'history'">
              歷史訂單
            </button>
          </li>
        </ul>
      </div>
      
      <div class="tab-content">
        <!-- 當前訂單 -->
        <div v-if="activeTab === 'current'" class="current-orders">
          <div v-if="loading" class="text-center my-5">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          
          <div v-else-if="currentOrders.length === 0" class="alert alert-info">
            目前沒有進行中的訂單
          </div>
          
          <div v-else class="order-list">
            <div v-for="order in currentOrders" :key="order.id" class="order-card">
              <div class="card mb-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">訂單 #{{ order.id }}</h5>
                  <span class="badge" :class="getStatusBadgeClass(order.status)">{{ getStatusText(order.status) }}</span>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6">
                      <p><strong>客戶名稱:</strong> {{ order.customerName }}</p>
                      <p><strong>預約日期:</strong> {{ order.appointmentDate }}</p>
                      <p><strong>預約時間:</strong> {{ order.appointmentTime }}</p>
                    </div>
                    <div class="col-md-6">
                      <p><strong>服務項目:</strong> {{ order.serviceName }}</p>
                      <p><strong>服務時長:</strong> {{ order.serviceTime }}</p>
                      <p><strong>訂單金額:</strong> NT$ {{ order.amount }}</p>
                    </div>
                  </div>
                  <div class="mt-3 d-flex justify-content-end">
                    <button class="btn btn-outline-primary me-2" @click="viewOrderDetails(order.id)">查看詳情</button>
                    <button v-if="order.status === 'pending'" class="btn btn-success me-2" @click="confirmOrder(order.id)">確認訂單</button>
                    <button v-if="['pending', 'confirmed'].includes(order.status)" class="btn btn-danger" @click="cancelOrder(order.id)">取消訂單</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 歷史訂單 -->
        <div v-if="activeTab === 'history'" class="history-orders">
          <div class="mb-3">
            <div class="row">
              <div class="col-md-4">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="搜尋訂單..." v-model="searchQuery">
                  <button class="btn btn-outline-secondary" type="button" @click="searchOrders">搜尋</button>
                </div>
              </div>
              <div class="col-md-4">
                <select class="form-select" v-model="filterStatus">
                  <option value="">所有狀態</option>
                  <option value="completed">已完成</option>
                  <option value="cancelled">已取消</option>
                </select>
              </div>
              <div class="col-md-4">
                <div class="input-group">
                  <input type="date" class="form-control" v-model="filterDate">
                  <button class="btn btn-outline-secondary" type="button" @click="resetFilters">重置</button>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="loading" class="text-center my-5">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          
          <div v-else-if="historyOrders.length === 0" class="alert alert-info">
            沒有符合條件的歷史訂單
          </div>
          
          <div v-else class="order-list">
            <div v-for="order in historyOrders" :key="order.id" class="order-card">
              <div class="card mb-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">訂單 #{{ order.id }}</h5>
                  <span class="badge" :class="getStatusBadgeClass(order.status)">{{ getStatusText(order.status) }}</span>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6">
                      <p><strong>客戶名稱:</strong> {{ order.customerName }}</p>
                      <p><strong>預約日期:</strong> {{ order.appointmentDate }}</p>
                      <p><strong>完成日期:</strong> {{ order.completedDate || '---' }}</p>
                    </div>
                    <div class="col-md-6">
                      <p><strong>服務項目:</strong> {{ order.serviceName }}</p>
                      <p><strong>訂單金額:</strong> NT$ {{ order.amount }}</p>
                      <p><strong>付款方式:</strong> {{ order.paymentMethod }}</p>
                    </div>
                  </div>
                  <div class="mt-3 d-flex justify-content-end">
                    <button class="btn btn-outline-primary" @click="viewOrderDetails(order.id)">查看詳情</button>
                  </div>
                </div>
              </div>
            </div>
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
  name: 'OrderView',
  components: {
    SitemapNavBar
  },
  setup() {
    const router = useRouter();
    const activeTab = ref('current');
    const loading = ref(true);
    const currentOrders = ref([]);
    const historyOrders = ref([]);
    const searchQuery = ref('');
    const filterStatus = ref('');
    const filterDate = ref('');
    
    // 處理登出
    const handleLogout = () => {
      console.log('用戶登出');
      router.push('/login');
    };
    
    // 獲取當前訂單
    const fetchCurrentOrders = async () => {
      try {
        loading.value = true;
        const response = await axios.get('/api/order/current_orders/');
        if (response.data.success) {
          currentOrders.value = response.data.orders;
        }
      } catch (error) {
        console.error('獲取當前訂單失敗:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // 獲取歷史訂單
    const fetchHistoryOrders = async () => {
      try {
        loading.value = true;
        const params = {};
        if (searchQuery.value) params.query = searchQuery.value;
        if (filterStatus.value) params.status = filterStatus.value;
        if (filterDate.value) params.date = filterDate.value;
        
        const response = await axios.get('/api/order/history_orders/', { params });
        if (response.data.success) {
          historyOrders.value = response.data.orders;
        }
      } catch (error) {
        console.error('獲取歷史訂單失敗:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // 確認訂單
    const confirmOrder = async (orderId) => {
      try {
        const response = await axios.post(`/api/order/confirm_order/${orderId}/`);
        if (response.data.success) {
          // 刷新訂單列表
          fetchCurrentOrders();
        }
      } catch (error) {
        console.error('確認訂單失敗:', error);
      }
    };
    
    // 取消訂單
    const cancelOrder = async (orderId) => {
      if (!confirm('確定要取消此訂單嗎？')) return;
      
      try {
        const response = await axios.post(`/api/order/cancel_order/${orderId}/`);
        if (response.data.success) {
          // 刷新訂單列表
          fetchCurrentOrders();
        }
      } catch (error) {
        console.error('取消訂單失敗:', error);
      }
    };
    
    // 查看訂單詳情
    const viewOrderDetails = (orderId) => {
      // 導航到訂單詳情頁面
      // router.push(`/orders/${orderId}`);
      alert(`查看訂單 ${orderId} 的詳情`);
    };
    
    // 搜尋訂單
    const searchOrders = () => {
      fetchHistoryOrders();
    };
    
    // 重置篩選條件
    const resetFilters = () => {
      searchQuery.value = '';
      filterStatus.value = '';
      filterDate.value = '';
      fetchHistoryOrders();
    };
    
    // 獲取訂單狀態文字
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待確認',
        'confirmed': '已確認',
        'completed': '已完成',
        'cancelled': '已取消'
      };
      return statusMap[status] || status;
    };
    
    // 獲取訂單狀態徽章樣式
    const getStatusBadgeClass = (status) => {
      const classMap = {
        'pending': 'bg-warning',
        'confirmed': 'bg-primary',
        'completed': 'bg-success',
        'cancelled': 'bg-danger'
      };
      return classMap[status] || 'bg-secondary';
    };
    
    onMounted(() => {
      fetchCurrentOrders();
      fetchHistoryOrders();
    });
    
    return {
      activeTab,
      loading,
      currentOrders,
      historyOrders,
      searchQuery,
      filterStatus,
      filterDate,
      confirmOrder,
      cancelOrder,
      viewOrderDetails,
      searchOrders,
      resetFilters,
      getStatusText,
      getStatusBadgeClass,
      handleLogout
    };
  }
}
</script>

<style scoped>
.order-view {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: var(--primary-color);
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.order-card {
  transition: transform 0.2s;
}

.order-card:hover {
  transform: translateY(-3px);
}

.card-header {
  background-color: #f8f9fa;
}

.badge {
  font-size: 0.8rem;
  padding: 0.5em 0.7em;
}
</style>
