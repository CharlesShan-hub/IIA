<template>
  <div 
    v-if="notification.error || notification.success"
    :class="['notification-container', notification.error ? 'error' : 'success']"
    role="alert"
  >
    <span>{{ notification.error || notification.success }}</span>
    <button type="button" class="close-btn" @click="clearNotification">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
</template>

<script>
import { useNotificationStore } from '@/stores/notification'
import { onMounted } from 'vue'

export default {
  name: 'AppNotification',
  setup() {
    const notificationStore = useNotificationStore()
    
    // 自动清除通知的函数
    const autoClearNotification = () => {
      if (notificationStore.error || notificationStore.success) {
        setTimeout(() => {
          notificationStore.clear()
        }, 3000) // 3秒后自动清除
      }
    }
    
    // 监听通知变化
    onMounted(() => {
      autoClearNotification()
      
      // 在组件挂载后，如果通知状态变化，重新设置自动清除定时器
      const unwatch = notificationStore.$subscribe(() => {
        autoClearNotification()
      })
      
      // 组件卸载时取消订阅
      return () => unwatch()
    })
    
    return {
      notification: notificationStore,
      clearNotification: notificationStore.clear
    }
  }
}
</script>

<style scoped>
/* 通知容器样式 */
.notification-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  min-width: 300px;
  max-width: 500px;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  display: flex;
  align-items: center;
  animation: slideDown 0.3s ease-out forwards;
}

/* 成功和错误状态样式 */
.notification-container.success {
  background-color: #d4edda;
  color: #155724;
}

.notification-container.error {
  background-color: #f8d7da;
  color: #721c24;
}

/* 关闭按钮样式 */
.close-btn {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  line-height: 1;
  color: inherit;
  opacity: 0.7;
  transition: all 0.2s ease;
  margin-left: auto;
  cursor: pointer;
}

.close-btn:hover {
  opacity: 1;
}

/* 通知内容样式 */
.notification-container span {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.4;
}

/* 滑入动画 */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translate(-50%, -20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .notification-container {
    margin: 0 15px;
    max-width: calc(100% - 30px);
  }
}
</style>