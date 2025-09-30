<template>
  <div class="card shadow-none">
    <div class="card-block">
      <div class="account-box">
        <div class="card-box shadow-none p-4">
          <div class="p-2">
            <div class="text-center mt-4">
              <img src="@/assets/images/logo-dark.png" height="40" alt="logo">
            </div>

            <h4 class="font-size-18 mt-5 text-center">Welcome Back !</h4>
            <p class="text-muted text-center">Sign in to continue to IIA.</p>

            <!-- 邮箱输入 -->
            <div class="form-group">
              <label for="mail">Email</label>
              <input 
                v-model="form.email" 
                type="email" 
                class="form-control" 
                placeholder="Enter email"
                :disabled="isLoggingIn"
              >
            </div>

            <!-- 密码输入 -->
            <div class="form-group">
              <label for="password">Password</label>
              <input 
                v-model="form.password" 
                type="password" 
                class="form-control" 
                placeholder="Enter password"
                :disabled="isLoggingIn"
                @keyup.enter="handleLogin"
              >
            </div>

            <!-- 记住我 & 登录按钮 -->
            <div class="form-group row">
              <div class="col-sm-6">
                <div class="custom-control custom-checkbox">
                  <input 
                    v-model="form.remember" 
                    type="checkbox" 
                    class="custom-control-input" 
                    id="remember"
                    :disabled="isLoggingIn"
                  >
                  <label class="custom-control-label" for="remember">Remember me</label>
                </div>
              </div>
              <div class="col-sm-6 text-right">
                <button 
                  @click="handleLogin"
                  class="btn btn-primary w-md waves-effect waves-light"
                  :disabled="isLoggingIn"
                >
                  <span v-if="isLoggingIn">
                    <i class="fas fa-spinner fa-spin"></i> Logging in...
                  </span>
                  <span v-else>Log In</span>
                </button>
              </div>
            </div>

            <!-- 忘记密码链接 -->
            <div class="form-group mt-2 mb-0 row">
              <div class="col-12 mt-3">
                <router-link to="/auth/forgot-password">
                  <i class="mdi mdi-lock"></i> Forgot your password?
                </router-link>
              </div>
            </div>

            <!-- 注册引导 -->
            <div class="mt-4 pt-4 text-center">
              <p>Don't have an account ? 
                <router-link to="/auth/register" class="font-weight-medium text-primary">Signup now</router-link>
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
import { useAuthStore } from '@/stores/auth'; // Pinia状态管理
import { useNotificationStore } from '@/stores/notification'; // 导入通知store
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'LoginPage',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const isLoggingIn = ref(false);
    const form = reactive({
      email: '',
      password: '',
      remember: false
    });
    
    // 获取通知方法
    const notificationStore = useNotificationStore();
    const { success, error } = notificationStore;
    
    const handleLogin = async () => {
      // 基础表单验证
      if (!form.email || !form.password) {
        error('Email and password are required');
        return;
      }

      isLoggingIn.value = true;
      
      try {
        // 调用登录接口
        const data = await axios.post('/api/auth/login', {
          email: form.email,
          password: form.password
        });

        // 使用Pinia存储登录状态
        authStore.login({
          token: data.token,
          user: data.user
        });

        // 记住我功能
        if (form.remember) {
          localStorage.setItem('rememberedEmail', form.email);
        } else {
          localStorage.removeItem('rememberedEmail');
        }

        // 跳转到首页
        router.push('/main');
        success('Login successful!');

      } catch (error) {
        // 错误处理
        const errorMsg = error.response?.data?.message || 'Login failed';
        error(errorMsg);
      } finally {
        isLoggingIn.value = false;
      }
    };
    
    // 自动填充记住的邮箱
    onMounted(() => {
      const rememberedEmail = localStorage.getItem('rememberedEmail');
      if (rememberedEmail) {
        form.email = rememberedEmail;
        form.remember = true;
      }
    });
    
    return {
      authStore,
      form,
      isLoggingIn,
      handleLogin,
      error,
      success
    }
  }
}
</script>

<style scoped>
/* 按钮加载状态 */
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 调整登录卡片宽度，与Admin项目样式保持一致 */
.card {
  max-width: 420px; /* 与Admin项目中的.account-page-full宽度一致 */
  margin: 0 auto;
}

/* 响应式调整 */
@media (max-width: 576px) {
  .col-sm-6 {
    width: 100%;
    margin-bottom: 10px;
  }
  .text-right {
    text-align: left !important;
  }
  .card {
    max-width: 100%;
    margin: 0 15px;
  }
}
</style>