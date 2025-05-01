<template>
  <div>
    <!-- 日曆容器 -->
    <div class="container caledar-loading" id="calendar-container">
      <div class="text-center" v-if="loading">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div ref="calendarRef"></div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import moment from 'moment';

export default {
  name: 'BookedCalendar',
  setup() {
    const loading = ref(true);
    const calendarRef = ref(null);
    let calendar = null;
    
    // 初始化日曆
    const initCalendar = () => {
      calendar = new FullCalendar.Calendar(calendarRef.value, {
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
        }
      });
      calendar.render();
    };
    
    // 引入 API 服務
    import { getAppointmentTimes } from '../api/calendar';
    
    // 獲取預約數據
    const fetchAppointments = async () => {
      try {
        const data = await getAppointmentTimes();
        
        if (data.success) {
          const appointmentList = data.appointment_time;
          if (!appointmentList.length) {
            loading.value = false;
            return;
          }
          
          appointmentList.forEach(appointment => {
            // 設定選擇的日期和時間
            let selectedDate = `${appointment.appointmentDate}`;
            let selectedTime = `${appointment.appointmentTime}`;
            
            // 設定事件起始時間
            let startDate = selectedDate + 'T' + selectedTime;
            
            // 依商家服務時間的總長設定每個預約時段的結束時間
            let endDate;
            if (appointment.appointmentTotalTime.includes("小時")) {
              let hour = Number(parseInt(appointment.appointmentTotalTime, 10));
              endDate = moment(startDate).add(hour, 'hours').format('YYYY-MM-DDTHH:mm');
            } else if (appointment.appointmentTotalTime.includes("分")) {
              let minute = Number(parseInt(appointment.appointmentTotalTime, 10));
              endDate = moment(startDate).add(minute, 'minutes').format('YYYY-MM-DDTHH:mm');
            } else {
              let day = Number(parseInt(appointment.appointmentTotalTime, 10));
              endDate = moment(startDate).add(day, 'days').format('YYYY-MM-DDTHH:mm');
            }
            
            // 新建一個事件對象
            let newEvent = {
              title: `${appointment.consumerName}`,
              start: startDate,
              end: endDate
            };
            
            // 將事件添加到FullCalendar
            calendar.addEvent(newEvent);
          });
          
          loading.value = false;
        }
      } catch (error) {
        console.error('獲取預約數據時出錯:', error);
        loading.value = false;
      }
    };
    
    onMounted(() => {
      initCalendar();
      fetchAppointments();
    });
    
    return {
      loading,
      calendarRef
    };
  }
}
</script>

<style scoped>
.caledar-loading {
  margin-top: 20px;
}
</style>
