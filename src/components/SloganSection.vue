<template>
  <div id="slogan-container">
    <div class="slogan">消費者LINE預約<img src="https://messagespic.s3.us-west-2.amazonaws.com/schedulebooking/static/images/LINE.png" class="line-icon"><br>商家省時又省心</div>
    <div class="start-btn"><button type="button" class="btn btn-outline-primary" id="btn-literal" @click="$emit('redirect-login')">Let's Start</button></div>
  </div>
</template>

<script>
export default {
  name: 'SloganSection',
  emits: ['redirect-login']
}
</script>

<style scoped>
#slogan-container {
  background-color: #C3A6A0;
  padding-top: 60px;
  padding-bottom: 30px;
  margin-top: 56px; /* 為固定導航欄留出空間 */
}

.start-btn {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.slogan {
  font-family: "Microsoft Jhenghei";
  font-weight: bold;
  padding-top: 130px;
  font-size: 40px;
  text-align: center;
}

.line-icon {
  width: 45px;
  margin-left: 5px;
  box-shadow: 8px 8px 5px rgba(0, 0, 0, 0.2);
}

#btn-literal {
  font-family: "Microsoft Jhenghei";
  font-size: 30px;
}
</style>
