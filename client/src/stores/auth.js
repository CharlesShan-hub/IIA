import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    login(data) {
      this.token = data.token;
      this.user = data.user;
      this.isAuthenticated = true;
      
      // 保存到本地存储
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
    },

    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      
      // 清除本地存储
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('rememberedEmail');
    },

    // 更新用户信息
    updateUser(userData) {
      this.user = { ...this.user, ...userData };
      localStorage.setItem('user', JSON.stringify(this.user));
    }
  }
});