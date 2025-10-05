<template>
  <div class="card shadow-none">
    <div class="card-block">
      <div class="account-box">
        <div class="card-box shadow-none p-4">
          <div class="p-2">
            <div class="text-center mt-4">
              <img src="@/assets/images/logo-dark.png" height="40" alt="logo">
            </div>

            <h4 class="font-size-18 mt-5 text-center">Free Register</h4>

            <!-- 邮箱输入 -->
            <div class="form-group">
              <label for="useremail">Email</label>
              <input 
                v-model="form.email" 
                type="email" 
                class="form-control" 
                placeholder="Enter email"
                :disabled="isSending"
              >
            </div>

            <!-- 验证码输入 -->
            <div class="form-group">
              <label for="code">Validation Code</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input 
                    v-model="form.code" 
                    type="text" 
                    class="form-control" 
                    placeholder="6-digit code"
                    maxlength="6"
                  >
                </div>
                <div class="col-md-4 col-4">
                  <button 
                    class="btn btn-primary btn-block" 
                    @click="requestCode"
                    :disabled="isSending || !form.email"
                  >
                    {{ countdown > 0 ? `${countdown}s` : 'Send' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 用户昵称 -->
            <div class="form-group">
              <label for="nickname">Nickname</label>
              <input 
                v-model="form.nickname" 
                type="text" 
                class="form-control" 
                placeholder="Enter nickname"
              >
            </div>

            <!-- 密码 -->
            <div class="form-group">
              <label for="userpassword">Password</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input 
                    v-model="form.password" 
                    type="password" 
                    class="form-control" 
                    placeholder="At least 6 characters"
                  >
                </div>
                <div class="col-md-4 col-4">
                  <button 
                    class="btn btn-primary w-md waves-effect waves-light" 
                    @click="handleRegister"
                    :disabled="isRegistering"
                  >
                    Register
                  </button>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-4 text-center">
              <p>Already have an account ? 
                <router-link to="/auth/login" class="font-weight-medium text-primary">Login</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'RegisterPage',
  setup() {
    const authStore = useAuthStore();
    const notificationStore = useNotificationStore();
    const router = useRouter();
    
    const form = reactive({
      email: '',
      code: '',
      nickname: '',
      password: ''
    });
    
    const countdown = ref(0);
    const isSending = ref(false);
    const isRegistering = ref(false);
    
    // 获取通知方法
    const { success, error } = notificationStore;
    
    // 发送验证码
    const requestCode = async () => {
      if (!form.email) {
        error('Please enter email');
        return;
      }

      isSending.value = true;
      try {
        await axios.post('/api/auth/send-code', { 
          email: form.email 
        });
        success('Verification code sent');
        startCountdown();
      } catch (err) {
        error(err.response?.data?.message || 'Failed to send code');
      } finally {
        isSending.value = false;
      }
    };

    // 注册提交
    const handleRegister = async () => {
      if (!validateForm()) return;

      isRegistering.value = true;
      try {
        const data = await axios.post('/api/auth/register', {
          email: form.email,
          code: form.code,
          nickname: form.nickname,
          password: form.password
        });
        
        // 使用Pinia存储登录状态
        authStore.login({
          token: data.token,
          user: data.userInfo
        });
        
        success('Registration successful!');
        router.push('/main');
      } catch (err) {
        error(err.response?.data?.message || 'Registration failed');
      } finally {
        isRegistering.value = false;
      }
    };

    // 表单验证
    const validateForm = () => {
      if (!form.email) {
        error('Email is required');
        return false;
      }
      if (!form.code) {
        error('Verification code is required');
        return false;
      }
      if (!form.nickname) {
        error('Nickname is required');
        return false;
      }
      if (form.password.length < 6) {
        error('Password must be at least 6 characters');
        return false;
      }
      return true;
    };

    // 验证码倒计时
    const startCountdown = () => {
      countdown.value = 60;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
        }
      }, 1000);
    };
    
    return {
      form,
      countdown,
      isSending,
      isRegistering,
      requestCode,
      handleRegister,
      validateForm,
      startCountdown,
      success,
      error
    }
  }
}
</script>

<style scoped>
/* 按钮禁用样式 */
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .col-md-8, .col-md-4 {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>