<template>
  <div>
    <!-- 使用之前創建的 SitemapNavBar 組件 -->
    <sitemap-nav-bar @logout="handleLogout" />
    
    <!-- 日曆容器 -->
    <div class="container" id="calendar-container">
      <!-- 加載指示器 -->
      <div class="text-center loading-overlay" v-if="isLoading">
        <div class="spinner-container">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
      
      <!-- 日曆標題 -->
      <div class="calendar-header">
        <h2>預約行事曆</h2>
        <p>查看和管理您的所有預約</p>
      </div>
      
      <!-- 日曆視圖 -->
      <div class="calendar-card">
        <div ref="calendar"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import SitemapNavBar from '@/components/SitemapNavBar.vue';

export default {
  name: 'BookedCalendarView',
  components: {
    SitemapNavBar
  },
  setup() {
    const router = useRouter();
    const calendar = ref(null);
    const isLoading = ref(true);
    const calendarInstance = ref(null);
    
    // 模擬從API獲取的預約數據
    const appointmentData = reactive([
      {
        consumerName: '王小明',
        appointmentDate: '2025-05-02',
        appointmentTime: '09:00',
        appointmentTotalTime: '1小時'
      },
      {
        consumerName: '李小花',
        appointmentDate: '2025-05-02',
        appointmentTime: '14:00',
        appointmentTotalTime: '30分'
      },
      {
        consumerName: '張大山',
        appointmentDate: '2025-05-03',
        appointmentTime: '10:00',
        appointmentTotalTime: '2小時'
      }
    ]);
    
    // 處理登出
    const handleLogout = () => {
      console.log('用戶登出');
      router.push('/login');
    };
    
    // 初始化日曆
    const initCalendar = () => {
      if (!calendar.value) return;
      
      // 使用 FullCalendar 創建日曆
      calendarInstance.value = new FullCalendar.Calendar(calendar.value, {
        themeSystem: 'bootstrap5',
        initialView: 'timeGridWeek',
        timeZone: 'Asia/Taipei',
        height: 650,
        fixedWeekCount: false,
        showNonCurrentDates: false,
        allDaySlot: false,
        headerToolbar: {
          left: 'prev,next',
          center: 'title',
          right: 'today timeGridWeek,timeGridDay'
        },
        buttonText: {
          today: '今天',
          week: '週',
          day: '日'
        },
        locale: 'zh-tw',
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }
      });
      
      // 渲染日曆
      calendarInstance.value.render();
      
      // 添加預約事件到日曆
      loadAppointments();
    };
    
    // 加載預約數據
    const loadAppointments = () => {
      // 實際應用中，這裡應該是從API獲取數據
      // fetch('/order/get_appointment_time/').then(...)
      
      // 使用模擬數據
      setTimeout(() => {
        appointmentData.forEach(appointment => {
          // 設置日期和時間
          const selectedDate = appointment.appointmentDate;
          const selectedTime = appointment.appointmentTime;
          
          // 設置事件起始時間
          const startDate = `${selectedDate}T${selectedTime}`;
          
          // 計算結束時間
          let endDate;
          if (appointment.appointmentTotalTime.includes('小時')) {
            const hour = Number(parseInt(appointment.appointmentTotalTime, 10));
            endDate = moment(startDate).add(hour, 'hours').format('YYYY-MM-DDTHH:mm');
          } else if (appointment.appointmentTotalTime.includes('分')) {
            const minute = Number(parseInt(appointment.appointmentTotalTime, 10));
            endDate = moment(startDate).add(minute, 'minutes').format('YYYY-MM-DDTHH:mm');
          } else {
            const day = Number(parseInt(appointment.appointmentTotalTime, 10));
            endDate = moment(startDate).add(day, 'days').format('YYYY-MM-DDTHH:mm');
          }
          
          // 創建新事件
          const newEvent = {
            title: appointment.consumerName,
            start: startDate,
            end: endDate,
            backgroundColor: getRandomColor(),
            borderColor: 'transparent',
            textColor: '#fff'
          };
          
          // 添加事件到日曆
          calendarInstance.value.addEvent(newEvent);
        });
        
        // 隱藏加載指示器
        isLoading.value = false;
      }, 1000); // 模擬網絡延遲
    };
    
    // 生成隨機顏色
    const getRandomColor = () => {
      const colors = [
        '#4285F4', // Google Blue
        '#34A853', // Google Green
        '#FBBC05', // Google Yellow
        '#EA4335', // Google Red
        '#5E35B1', // Deep Purple
        '#00897B', // Teal
        '#C0CA33', // Lime
        '#FB8C00', // Orange
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    };
    
    // 組件掛載後初始化日曆
    onMounted(() => {
      initCalendar();
    });
    
    return {
      calendar,
      isLoading,
      handleLogout
    };
  }
}
</script>

<style scoped>
/* 基本樣式 */
:deep(body) {
  background-color: #f7f1f0;
  font-family: "Microsoft Jhenghei", sans-serif;
}

/* 日曆容器樣式 */
#calendar-container {
  margin-top: 30px;
  position: relative;
  padding: 0 20px;
  max-width: 1200px;
}

/* 加載指示器樣式 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(247, 241, 240, 0.8);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
}

.spinner-container {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  color: #3498db;
}

/* 日曆標題樣式 */
.calendar-header {
  text-align: center;
  margin-bottom: 20px;
}

.calendar-header h2 {
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 5px;
}

.calendar-header p {
  color: #7f8c8d;
  font-size: 16px;
}

/* 日曆卡片樣式 */
.calendar-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 30px;
}

/* FullCalendar 自定義樣式 */
:deep(.fc) {
  font-family: 'Microsoft Jhenghei', sans-serif;
}

:deep(.fc-toolbar-title) {
  font-size: 1.5rem !important;
  font-weight: 700;
  color: #2c3e50;
}

:deep(.fc-button-primary) {
  background-color: #3498db;
  border-color: #3498db;
  transition: all 0.3s ease;
}

:deep(.fc-button-primary:hover) {
  background-color: #2980b9;
  border-color: #2980b9;
}

:deep(.fc-button-active) {
  background-color: #2980b9 !important;
  border-color: #2980b9 !important;
}

:deep(.fc-daygrid-day-number), :deep(.fc-col-header-cell-cushion) {
  font-family: 'Microsoft Jhenghei', sans-serif;
  color: #2c3e50;
  text-decoration: none;
}

:deep(.fc-event) {
  border-radius: 4px;
  padding: 2px 4px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

:deep(.fc-timegrid-slot-label) {
  font-size: 0.85rem;
}

:deep(.fc-timegrid-axis-cushion) {
  font-weight: 500;
}

:deep(.fc-day-today) {
  background-color: rgba(52, 152, 219, 0.1) !important;
}

/* 響應式設計 */
@media (max-width: 768px) {
  #calendar-container {
    padding: 0 10px;
  }
  
  :deep(.fc-toolbar) {
    flex-direction: column;
  }
  
  :deep(.fc-toolbar-chunk) {
    margin-bottom: 10px;
  }
}
</style>
