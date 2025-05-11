import { createRouter, createWebHistory } from 'vue-router'
import AuthPage from '../components/Auth.vue'
import LoginPage from '../components/Login.vue'
import RegisterPage from '../components/Register.vue'
import ForgotPasswordPage from '../components/ForgotPassword.vue'
import MainPage from '../components/Main.vue'

const routes = [
  {
    path: '/auth',
    component: AuthPage,
    children: [
      { path: 'login', component: LoginPage },
      { path: 'register', component: RegisterPage },
      { path: 'forgot-password', component: ForgotPasswordPage }
    ]
  },
  { 
    path: '/main', 
    component: MainPage 
  },
  { 
    path: '/', 
    // redirect: '/auth/login',
    redirect: '/main' 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router