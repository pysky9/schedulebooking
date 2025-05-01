<template>
  <div>
    <home-nav-bar @redirect-login="redirectToLogin" />
    <slogan-section @redirect-login="redirectToLogin" />
    <feature-section />
    <footer-section />
  </div>
</template>

<script>
import HomeNavBar from '@/components/HomeNavBar.vue';
import SloganSection from '@/components/SloganSection.vue';
import FeatureSection from '@/components/FeatureSection.vue';
import FooterSection from '@/components/FooterSection.vue';

export default {
  name: 'IndexView',
  components: {
    HomeNavBar,
    SloganSection,
    FeatureSection,
    FooterSection
  },
  methods: {
    redirectToLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  background-color: #f7f1f0;
  font-family: "Microsoft Jhenghei";
}
</style>
