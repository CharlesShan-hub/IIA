// 通知状态管理
import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    type: null,
    message: null
  }),
  
  actions: {
    success(message) {
      this.type = 'alert-success'
      this.message = message
    },
    
    error(message) {
      this.type = 'alert-danger'
      this.message = message
    },
    
    clear() {
      this.type = null
      this.message = null
    }
  }
})