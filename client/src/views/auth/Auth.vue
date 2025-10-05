<template>
  <div class="account-pages">
    <img class="accountbg" src="@/assets/images/bg.jpg" alt="background">
    <div class="wrapper-page account-page-full">
      <router-view></router-view>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AppFooter from '@/components/main/Footer.vue'

export default {
  name: 'AuthPage',
  components: {
    AppFooter,
  },
  data() {
    return {
      year: new Date().getFullYear()
    }
  },
  provide() {
    return {
      year: this.year
    }
  }
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

.footer {
  left: 0 !important;
  width: 100%;
}
</style>