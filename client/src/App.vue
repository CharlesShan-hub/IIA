<template>
  <div id="app">
    <router-view></router-view>
    <!-- 全局通知组件 -->
    <AppNotification />
  </div>
</template>

<script>
import AppNotification from './components/main/Notification.vue'

const AppComponent = {
  name: 'App',
  components: {
    AppNotification
  }
}

export default AppComponent
export const App = AppComponent
</script>
