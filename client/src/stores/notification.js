// 通知状态管理
import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    error: null,
    success: null
  }),
  
  actions: {
    success(message) {
      this.success = message
      this.error = null
    },
    
    error(message) {
      this.error = message
      this.success = null
    },
    
    clear() {
      this.error = null
      this.success = null
    }
  }
})