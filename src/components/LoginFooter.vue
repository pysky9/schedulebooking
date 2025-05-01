<template>
  <div class="footer">
    <div class="footerContent">COPYRIGHT @ {{ currentYear }} 吉時約 </div>
  </div>
</template>

<script>
export default {
  name: 'LoginFooter',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.footer {
  display: flex;
  height: 104px;
  justify-content: center;
  background: #AA7052;
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
  margin-top: 150px;
}

.footerContent {
  flex: none;
  line-height: 104px; 
  font-family: "Microsoft Jhenghei";
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  color: #FFFFFF;
  text-align: center;
}
</style>
