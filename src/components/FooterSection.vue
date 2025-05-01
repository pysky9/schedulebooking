<template>
  <div class="footer">
    <div class="footerContent">COPYRIGHT @ {{ currentYear }} 吉時約 </div>
  </div>
</template>

<script>
export default {
  name: 'FooterSection',
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
  background-color: #AA7052;
}

.footerContent {
  flex: none;
  line-height: 104px;
  font-family: "Microsoft Jhenghei";
  font-style: normal;
  font-weight: bold;
  font-size: 22px;
  text-align: center;
  color: white;
}
</style>
