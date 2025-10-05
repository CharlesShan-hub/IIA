<template>
  <div class="card shadow-none">
    <div class="card-block">
      <div class="account-box">
        <div class="card-box shadow-none p-4">
          <div class="p-2">
            <div class="text-center mt-4">
              <img src="@/assets/images/logo-dark.png" height="40" alt="logo">
            </div>

            <h4 class="font-size-18 mt-5 text-center">Reset Password</h4>

            <!-- 邮箱输入 -->
            <div class="form-group">
              <label for="useremail">Email</label>
              <input 
                v-model="form.email" 
                type="email" 
                class="form-control" 
                placeholder="Enter email"
                :disabled="isSendingCode || isResettingPassword"
              >
            </div>

            <!-- 验证码输入 -->
            <div class="form-group">
              <label for="verificationCode">Verification code</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input 
                    v-model="form.code" 
                    type="text" 
                    class="form-control" 
                    placeholder="Enter Verification Code"
                    :disabled="isSendingCode || isResettingPassword"
                  >
                </div>
                <div class="col-md-4 col-4">
                  <button 
                    class="btn btn-primary btn-block"
                    @click="sendCode"
                    :disabled="isSendingCode || countdown > 0 || isResettingPassword || !form.email"
                  >
                    {{ countdown > 0 ? `Resend in ${countdown}s` : 'Send' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 新密码输入 -->
            <div class="form-group">
              <label for="newPassword">New Password</label>
              <input 
                v-model="form.newPassword" 
                type="password" 
                class="form-control" 
                placeholder="New Password"
                :disabled="isSendingCode || isResettingPassword"
              >
            </div>

            <!-- 确认新密码输入 -->
            <div class="form-group">
              <label for="confirmPassword">Confirm New Password</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input 
                    v-model="form.confirmPassword" 
                    type="password" 
                    class="form-control" 
                    placeholder="Confirm New Password"
                    :disabled="isSendingCode || isResettingPassword"
                  >
                </div>
                <div class="col-md-4 col-4">
                  <button 
                    class="btn btn-primary btn-block"
                    @click="resetPassword"
                    :disabled="isSendingCode || isResettingPassword"
                  >
                    {{ isResettingPassword ? 'Resetting...' : 'Reset' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 登录链接 -->
            <div class="mt-4 pt-4 text-center">
              <p>Remember your password? <router-link to="/auth/login" class="font-weight-medium text-primary">Login now</router-link></p>
              <p class="mt-2">Don't have an account? <router-link to="/auth/register" class="font-weight-medium text-primary">Signup now</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '@/stores/notification';

export default {
  name: 'ForgotPasswordPage',
  setup() {
    const router = useRouter();
    const isSendingCode = ref(false);
    const isResettingPassword = ref(false);
    const countdown = ref(0);
    const form = reactive({
      email: '',
      code: '',
      newPassword: '',
      confirmPassword: ''
    });
    
    // 获取通知方法
    const notificationStore = useNotificationStore();
    const { success, error } = notificationStore;
    
    // 发送验证码
    const sendCode = async () => {
      if (!form.email) {
        error('Please enter email');
        return;
      }
      
      // 简单的邮箱格式验证
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(form.email)) {
        error('Please enter a valid email address');
        return;
      }
      
      isSendingCode.value = true;
      
      try {
        await axios.post('/api/auth/send-code', {
          email: form.email
        });
        
        success('Verification code sent successfully');
        startCountdown();
      } catch (err) {
        error(err.response?.data?.message || 'Failed to send verification code');
      } finally {
        isSendingCode.value = false;
      }
    };
    
    // 开始倒计时
    const startCountdown = () => {
      countdown.value = 60; // 60秒倒计时
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
        }
      }, 1000);
    };
    
    // 重置密码
    const resetPassword = async () => {
      // 表单验证
      if (!form.email || !form.code || !form.newPassword || !form.confirmPassword) {
        error('Please fill in all required fields');
        return;
      }
      
      // 验证邮箱格式
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(form.email)) {
        error('Please enter a valid email address');
        return;
      }
      
      // 验证密码长度
      if (form.newPassword.length < 6 || form.newPassword.length > 20) {
        error('Password length must be between 6 and 20 characters');
        return;
      }
      
      // 验证两次输入的密码是否一致
      if (form.newPassword !== form.confirmPassword) {
        error('Passwords do not match');
        return;
      }
      
      isResettingPassword.value = true;
      
      try {
        await axios.post('/api/auth/reset-password', {
          email: form.email,
          code: form.code,
          newPassword: form.newPassword
        });
        
        success('Password reset successfully');
        
        // 重置成功后跳转到登录页
        setTimeout(() => {
          router.push('/auth/login');
        }, 2000);
      } catch (err) {
        error(err.response?.data?.message || 'Failed to reset password');
      } finally {
        isResettingPassword.value = false;
      }
    };
    
    return {
      form,
      isSendingCode,
      isResettingPassword,
      countdown,
      sendCode,
      resetPassword,
      success,
      error
    };
  }
};
</script>

<style scoped>
/* 按钮加载状态 */
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 调整找回密码卡片宽度，与Admin项目样式保持一致 */
.card {
  max-width: 420px; /* 与Admin项目中的.account-page-full宽度一致 */
  margin: 0 auto;
}

/* 响应式调整 */
@media (max-width: 576px) {
  .col-md-8,
  .col-md-4,
  .col-8,
  .col-4 {
    width: 100%;
    margin-bottom: 10px;
  }
  .card {
    max-width: 100%;
    margin: 0 15px;
  }
}
</style>