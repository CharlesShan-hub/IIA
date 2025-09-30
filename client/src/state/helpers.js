// 状态管理辅助函数
import { mapActions } from 'pinia'

export const notificationMethods = mapActions('notification', ['success', 'error', 'clear'])