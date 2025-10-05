<template>
  <div class="app">
    <AppHeader />
    <div id="layout-wrapper">
      <AppSidebar />
      <div class="main-content">
        <DashboardPage />
        <AppFooter />
      </div>
    </div>
    <AppRightbar />
  </div>
</template>

<script>
import AppHeader from './Header.vue'
import AppSidebar from './Sidebar.vue'
import AppRightbar from './Rightbar.vue'
import AppFooter from './Footer.vue'
import DashboardPage from '../../views/Dashboard.vue'

export default {
  name: 'MainPage',
  components: {
    AppHeader,
    AppSidebar,
    AppRightbar,
    AppFooter,
    DashboardPage,
  },
}
</script>

<style scoped>
/* 从npm包导入bootstrap 5.0.1 */
@import 'bootstrap/dist/css/bootstrap.min.css';
@import '@/assets/css/icons.min.css';
@import '@/assets/css/app.min.css';
</style>
