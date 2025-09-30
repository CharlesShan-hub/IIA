<template>
  <div id="app">
    <router-view></router-view>
    <!-- 全局通知组件 -->
    <AppNotification />
  </div>
</template>

<script>
import AppNotification from './components/Notification.vue'

export default {
  name: 'App',
  components: {
    AppNotification
  }
}
</script>
