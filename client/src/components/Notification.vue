<template>
  <div 
    v-if="notification.message" 
    :class="['alert', notification.type, 'alert-dismissible fade show p-4 rounded-lg shadow-lg border-0', 'fixed-top d-flex mt-5 z-50 max-w-md mx-auto']"
    role="alert"
  >
    <span>{{ notification.message }}</span>
    <button type="button" class="close ml-auto" @click="clearNotification">
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
      if (notificationStore.message) {
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
/* 精美的通知样式 - 保持原有颜色 */
.alert {
  min-width: 300px;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(-10px);
  opacity: 0;
}

.alert.show {
  transform: translateY(0);
  opacity: 1;
}

/* 关闭按钮样式 */
.close {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  line-height: 1;
  color: inherit;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.close:hover {
  opacity: 1;
}

/* 通知内容样式 */
.alert span {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.4;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .alert {
    margin: 0 15px;
    max-width: calc(100% - 30px);
  }
}
</style>