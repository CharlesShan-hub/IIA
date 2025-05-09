<template>
  <div class="account-pages">
    <img class="accountbg" src="@/assets/images/bg.jpg" alt="background">
    <div class="wrapper-page account-page-full">
      <router-view></router-view>
      <AppFooter />
    </div>
  </div>
</template>

<script>
import AppFooter from './Footer.vue'

export default {
  name: 'AuthPage',
  components: {
    AppFooter,
  },
}
</script>

<style scoped>
.accountbg {
  position: fixed;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
  left: 0;
  top: 0;
}

@import '@/assets/css/bootstrap.min.css';
@import '@/assets/css/icons.min.css';
@import '@/assets/css/app.min.css';

.footer {
  left: 0 !important;
  width: 100%;
}
</style>