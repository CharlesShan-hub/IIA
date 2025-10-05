import { createRouter, createWebHistory } from 'vue-router'
import AuthPage from '../views/auth/Auth.vue'
import LoginPage from '../views/auth/Login.vue'
import RegisterPage from '../views/auth/Register.vue'
import ForgotPasswordPage from '../views/auth/ForgotPassword.vue'
import MainPage from '../components/main/Main.vue'
import DashboardPage from '../views/Dashboard.vue'
import TestNotification from '../views/TestNotification.vue'

const routes = [
  {
    path: '/auth',
    component: AuthPage,
    children: [
      { path: 'login', component: LoginPage },
      { path: 'register', component: RegisterPage },
      { path: 'forgot-password', component: ForgotPasswordPage },
    ]
  },
  { 
    path: '/', 
    redirect: '/auth/login',
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
    path: '/test-notification',
    component: TestNotification
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export { router }