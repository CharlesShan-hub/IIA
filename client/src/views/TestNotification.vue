<template>
  <div class="test-container">
    <h1>Notification Test Page</h1>
    <div class="buttons-container">
      <button class="btn btn-success" @click="showSuccessNotification">Show Success Notification</button>
      <button class="btn btn-danger" @click="showErrorNotification">Show Error Notification</button>
      <button class="btn btn-secondary" @click="clearAllNotifications">Clear Notifications</button>
    </div>
  </div>
</template>

<script>
import { useNotificationStore } from '@/stores/notification'

export default {
  name: 'TestNotification',
  setup() {
    const notificationStore = useNotificationStore()
    
    const showSuccessNotification = () => {
      notificationStore.success = 'This is a success notification!'
    }
    
    const showErrorNotification = () => {
      notificationStore.error = 'This is an error notification!'
    }
    
    const clearAllNotifications = () => {
      notificationStore.clear()
    }
    
    return {
      showSuccessNotification,
      showErrorNotification,
      clearAllNotifications
    }
  }
}
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.buttons-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>