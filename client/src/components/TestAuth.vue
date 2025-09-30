<template>
  <div class="auth-test-container">
    <div class="auth-tabs">
      <button 
        @click="activeTab = 'login'" 
        :class="{ active: activeTab === 'login' }"
      >
        Login Test
      </button>
      <button 
        @click="activeTab = 'register'" 
        :class="{ active: activeTab === 'register' }"
      >
        Register Test
      </button>
    </div>

    <!-- Login Form -->
    <div v-if="activeTab === 'login'" class="auth-form">
      <h2>Login Test</h2>
      <div class="form-group">
        <label>Email</label>
        <input v-model="loginForm.email" type="email" placeholder="user@example.com">
      </div>
      <div class="form-group">
        <label>Password</label>
        <input v-model="loginForm.password" type="password" placeholder="Password">
      </div>
      <button @click="handleLogin" :disabled="isLoggingIn">
        {{ isLoggingIn ? 'Logging in...' : 'Login' }}
      </button>
      <div v-if="loginResult" class="result-box">
        <h4>Login Result:</h4>
        <pre>{{ loginResult }}</pre>
      </div>
    </div>

    <!-- Register Form -->
    <div v-if="activeTab === 'register'" class="auth-form">
      <h2>Register Test</h2>
      <div class="form-group">
          <label>Email</label>
          <input v-model="registerForm.email" type="email" placeholder="user@example.com">
        </div>
        <div class="form-group">
          <label>Verification Code</label>
          <div class="code-input">
            <input v-model="registerForm.code" type="text" placeholder="6-digit code">
            <button 
              @click="sendVerificationCode" 
              :disabled="isSendingCode || countdown > 0"
            >
              {{ countdown > 0 ? `Resend in ${countdown}s` : 'Get Code' }}
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>Nickname</label>
          <input v-model="registerForm.nickname" type="text" placeholder="Nickname">
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="registerForm.password" type="password" placeholder="Password">
        </div>
      <button @click="handleRegister" :disabled="isRegistering">
        {{ isRegistering ? 'Registering...' : 'Register' }}
      </button>
      <div v-if="registerResult" class="result-box">
        <h4>Register Result:</h4>
        <pre>{{ registerResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';

export default {
  name: 'AuthTestPage',
  data() {
    return {
      activeTab: 'login',
      loginForm: {
        email: 'test@example.com',
        password: 'password123'
      },
      registerForm: {
        email: 'newuser@example.com',
        code: '',
        nickname: 'NewUser',
        password: 'newpassword123'
      },
      loginResult: null,
      registerResult: null,
      isLoggingIn: false,
      isRegistering: false,
      isSendingCode: false,
      countdown: 0
    }
  },
  methods: {
    async handleLogin() {
      this.isLoggingIn = true;
      this.loginResult = null;
      
      try {
        const response = await axios.post('/api/auth/login', this.loginForm);
        this.loginResult = {
          status: 'success',
          data: response.data
        };
      } catch (error) {
        this.loginResult = {
          status: 'error',
          message: error.response?.data?.message || error.message
        };
      } finally {
        this.isLoggingIn = false;
      }
    },

    async handleRegister() {
      this.isRegistering = true;
      this.registerResult = null;
      
      try {
        // 确保提交的对象只包含后端需要的字段
        const registerData = {
          email: this.registerForm.email,
          code: this.registerForm.code,
          nickname: this.registerForm.nickname,
          password: this.registerForm.password
        };
        const response = await axios.post('/api/auth/register', registerData);
        this.registerResult = {
          status: 'success',
          data: response.data
        };
      } catch (error) {
        this.registerResult = {
          status: 'error',
          message: error.response?.data?.message || error.message
        };
      } finally {
        this.isRegistering = false;
      }
    },

    async sendVerificationCode() {
      if (!this.registerForm.email) {
        alert('Please enter email first');
        return;
      }

      this.isSendingCode = true;
      try {
        await axios.post('/api/auth/send-code', {
          email: this.registerForm.email
        });
        this.startCountdown();
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to send code');
      } finally {
        this.isSendingCode = false;
      }
    },

    startCountdown() {
      this.countdown = 60;
      const timer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(timer);
        }
      }, 1000);
    }
  }
}
</script>

<style scoped>
.auth-test-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.auth-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.auth-tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
}

.auth-tabs button.active {
  border-bottom: 2px solid #4285f4;
  color: #4285f4;
  font-weight: bold;
}

.auth-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.code-input {
  display: flex;
  gap: 10px;
}

.code-input input {
  flex: 1;
}

button {
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.result-box {
  margin-top: 20px;
  padding: 15px;
  background: white;
  border: 1px solid #eee;
  border-radius: 4px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
