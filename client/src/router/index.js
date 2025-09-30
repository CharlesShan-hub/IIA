import { createRouter, createWebHistory } from 'vue-router'
import AuthPage from '../components/Auth.vue'
import LoginPage from '../components/Login.vue'
import RegisterPage from '../components/Register.vue'
import TestAuthPage from '../components/TestAuth.vue'
import ForgotPasswordPage from '../components/ForgotPassword.vue'
import MainPage from '../components/Main.vue'
import DashboardPage from '../components/Dashboard.vue'

const routes = [
  {
    path: '/auth',
    component: AuthPage,
    children: [
      { path: 'login', component: LoginPage },
      { path: 'register', component: RegisterPage },
      { path: 'forgot-password', component: ForgotPasswordPage },
      { path: 'test-auth', component: TestAuthPage }
    ]
  },
  { 
    path: '/main', 
    component: MainPage 
  },
  { 
    path: '/dashboard', 
    component: DashboardPage 
  },
  { 
    path: '/', 
    redirect: '/auth/test-auth'
    // redirect: '/auth/login',
    // redirect: '/main' 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router