<template>
  <div>
    <section-container 
      id="line-description" 
      :title="'消費者預約、購物、付款，LINE官方帳號等你來'" 
      :titleClass="'line-info'"
      :hasSubtitle="false">
      <template #image>
        <div class="line-gif-container">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/OAbooking.PNG" class="line-gif">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/arrow.png">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/OAbooking.gif" class="line-gif">
        </div>
      </template>
    </section-container>

    <section-container 
      id="merchant-setting-info" 
      :title="'商家彈性設定預約時段'" 
      :titleClass="'setting-info'"
      :hasSubtitle="true">
      <template #subtitle>
        <span class="setting-subtitle">輕鬆安排服務服務日期與時段、每次服務時間、服務價錢、是否啟動折扣</span><br>
        <span class="setting-subtitle">設定後立即顯示於LINE官方帳號預約系統</span>
      </template>
      <template #image>
        <div class="setting-img-container">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/timeSetting.PNG" class="setting-img">
        </div>
      </template>
    </section-container>

    <section-container 
      id="merchant-changing-info" 
      :title="'商家隨時調整預約時段，彈性安排工作時間'" 
      :titleClass="'changing-info'"
      :hasSubtitle="false">
      <template #image>
        <div class="changing-gif-container">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/changeDelete.gif" class="setting-img">
        </div>
      </template>
    </section-container>

    <section-container 
      id="merchant-order-info" 
      :title="'隨時查看客戶訂單，即刻掌握付款進度'" 
      :titleClass="'order-info'"
      :hasSubtitle="true">
      <template #subtitle>
        <span class="setting-subtitle">完美紀錄，讓您交易無後顧之憂。</span>
      </template>
      <template #image>
        <div class="changing-gif-container">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/order.PNG" class="setting-img">
        </div>
      </template>
    </section-container>

    <section-container 
      id="merchant-calendar-info" 
      :title="'客戶預約即時顯示於網站行事曆，<br>讓您無時無刻掌握工作進度'" 
      :titleClass="'calendar-info'"
      :hasSubtitle="false">
      <template #image>
        <div class="changing-gif-container">
          <img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/calendar.PNG" class="setting-img">
        </div>
      </template>
    </section-container>
  </div>
</template>

<script>
import SectionContainer from './SectionContainer.vue';

export default {
  name: 'FeatureSection',
  components: {
    SectionContainer
  }
}
</script>

<style scoped>
#line-description, #merchant-changing-info, #merchant-calendar-info {
  background-color: #C3A6A0;
}

#merchant-setting-info, #merchant-order-info {
  background-color: #D0B9B4;
}

.line-gif-container, .setting-img-container {
  flex: none;
  width: 50%;
}

.line-gif {
  width: 150px;
  border-radius: 5px;
  box-shadow: 15px 15px 5px rgba(0, 0, 0, 0.2);
}

.setting-img {
  width: 650px;
  border-radius: 5px;
  box-shadow: 15px 15px 5px rgba(0, 0, 0, 0.2);
}

.setting-subtitle, .changing-subtitle {
  font-family: "Microsoft Jhenghei";
  font-weight: 500;
  padding-top: 5px;
  font-size: 20px;
}

.changing-gif-container {
  width: 650px;
}

@media (max-width: 768px) {
  .line-gif-container, .setting-img-container, .changing-gif-container {
    width: 100%;
    padding-left: 20px;
    padding-right: 20px;
    text-align: center;
  }
  
  .setting-img, .line-gif {
    width: 90%;
    max-width: 400px;
  }
}
</style>
