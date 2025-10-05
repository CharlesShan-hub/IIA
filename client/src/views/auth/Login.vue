<template>
  <div class="account-pages my-5 pt-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6 col-xl-4">
          <div class="card overflow-hidden">
            <div class="bg-primary">
              <div class="text-primary text-center p-4">
                <h5 class="text-white font-size-20">Welcome Back !</h5>
                <p class="text-white-50">Sign in to continue to IIA.</p>
                <a href="/" class="logo logo-admin">
                  <img
                    src="@/assets/images/logo-dark.png"
                    height="24"
                    alt="logo"
                  />
                </a>
              </div>
            </div>
            <div class="card-body p-4">
              <div class="p-3">
                <!-- 错误提示 -->
                <div 
                  v-if="error"
                  class="alert alert-danger mt-3"
                  role="alert"
                >
                  {{ error }}
                </div>

                <form
                  @submit.prevent="handleLogin"
                  class="form-horizontal mt-4"
                >
                  <!-- 邮箱输入 -->
                  <div
                    class="mb-3"
                  >
                    <label
                      class="form-label"
                      for="email"
                    >
                      Email
                    </label>
                    <input
                      id="email"
                      v-model="form.email"
                      type="email"
                      class="form-control"
                      :class="{ 'is-invalid': isSubmitted && !form.email }"
                      placeholder="Enter email"
                      :disabled="isLoggingIn"
                      @keyup.enter="handleLogin"
                    />
                    <div
                      v-if="isSubmitted && !form.email"
                      class="invalid-feedback d-block"
                    >
                      Email is required.
                    </div>
                    <div
                      v-else-if="isSubmitted && !isValidEmail(form.email)"
                      class="invalid-feedback d-block"
                    >
                      Please enter valid email.
                    </div>
                  </div>

                  <!-- 密码输入 -->
                  <div
                    class="mb-3"
                  >
                    <label
                      class="form-label"
                      for="password"
                    >
                      Password
                    </label>
                    <input
                      id="password"
                      v-model="form.password"
                      type="password"
                      class="form-control"
                      :class="{ 'is-invalid': isSubmitted && !form.password }"
                      placeholder="Enter password"
                      :disabled="isLoggingIn"
                      @keyup.enter="handleLogin"
                    />
                    <div
                      v-if="isSubmitted && !form.password"
                      class="invalid-feedback d-block"
                    >
                      Password is required.
                    </div>
                  </div>

                  <!-- 记住我 & 登录按钮 -->
                  <div class="form-group row">
                    <div class="col-sm-6">
                      <div class="form-check">
                        <input
                          v-model="form.remember"
                          type="checkbox"
                          class="form-check-input"
                          id="remember"
                          :disabled="isLoggingIn"
                        />
                        <label
                          class="form-check-label"
                          for="remember"
                        >
                          Remember me
                        </label>
                      </div>
                    </div>
                    <div class="col-sm-6 text-end">
                      <button
                        type="submit"
                        class="btn btn-primary w-md"
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
                  <div class="mt-2 mb-0 row">
                    <div class="col-12 mt-4">
                      <router-link to="/auth/forgot-password">
                        <i class="mdi mdi-lock"></i> Forgot your password?
                      </router-link>
                    </div>
                  </div>
                </form>
              </div>
            </div>
            <!-- end card-body -->
          </div>
          <!-- end card -->
          <div class="mt-5 text-center">
            <p>
              Don't have an account ?
              <router-link to="/auth/register" class="fw-medium text-primary">
                Signup now
              </router-link>
            </p>
          </div>
        </div>
        <!-- end col -->
      </div>
      <!-- end row -->
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'LoginPage',
  inject: ['year'],
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const isLoggingIn = ref(false);
    const isSubmitted = ref(false);
    const form = reactive({
      email: '',
      password: '',
      remember: false
    });
    
    // 获取通知方法
    const notificationStore = useNotificationStore();
    const { success, error } = notificationStore;
    
    // 邮箱验证函数
    const isValidEmail = (email) => {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(email).toLowerCase());
    };
    
    const handleLogin = async () => {
      isSubmitted.value = true;
      
      // 基础表单验证
      if (!form.email) {
        notificationStore.error('Email is required');
        return;
      }
      
      if (!isValidEmail(form.email)) {
        notificationStore.error('Please enter valid email');
        return;
      }
      
      if (!form.password) {
        notificationStore.error('Password is required');
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

        // 跳转到首页或重定向页面
        const redirectFrom = router.currentRoute.value.query.redirectFrom;
        router.push(redirectFrom || '/main');
        success('Login successful!');

      } catch (error) {
        // 错误处理
        const errorMsg = error.response?.data?.message || 'Login failed';
        notificationStore.error(errorMsg);
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
      form,
      isLoggingIn,
      isSubmitted,
      handleLogin,
      error,
      isValidEmail
    }
  }
}
</script>
