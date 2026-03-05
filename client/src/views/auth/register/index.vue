<template>
  <div class="login register">
    <LoginLeftView></LoginLeftView>
    <div class="right-wrap">
      <div class="header">
        <ArtLogo class="icon" />
        <h1>{{ systemName }}</h1>
      </div>
      <div class="login-wrap">
        <div class="form">
          <h3 class="title">{{ $t('register.title') }}</h3>
          <p class="sub-title">{{ $t('register.subTitle') }}</p>
          <ElForm ref="formRef" :model="formData" :rules="rules" label-position="top">
            <ElFormItem prop="email">
              <ElInput
                v-model.trim="formData.email"
                :placeholder="$t('register.placeholder[0]')"
              />
            </ElFormItem>

            <ElFormItem prop="verificationCode">
              <div style="display: flex; gap: 10px; width: 100%;">
                <ElInput
                  v-model.trim="formData.code"
                  :placeholder="$t('register.placeholder[1]')"
                  style="flex: 1; min-width: 0;"
                />
                <ElButton
                  :disabled="countdown > 0"
                  type="primary"
                  @click="sendVerificationCode"
                  style="width: 120px; flex-shrink: 0;"
                >
                  {{ countdown > 0 ? `${countdown}${$t('register.placeholder[2]')}` : $t('register.placeholder[3]') }}
                </ElButton>
              </div>
            </ElFormItem>

            <ElFormItem prop="username">
              <ElInput
                v-model.trim="formData.username"
                :placeholder="$t('register.placeholder[4]')"
                type="text"
                autocomplete="off"
              />
            </ElFormItem>

            <ElFormItem prop="password">
              <ElInput
                v-model.trim="formData.password"
                :placeholder="$t('register.placeholder[5]')"
                type="password"
                autocomplete="off"
                show-password
              />
            </ElFormItem>

            <ElFormItem prop="confirmPassword">
              <ElInput
                v-model.trim="formData.confirmPassword"
                :placeholder="$t('register.placeholder[6]')"
                type="password"
                autocomplete="off"
                @keyup.enter="register"
                show-password
              />
            </ElFormItem>

            <ElFormItem prop="agreement">
              <ElCheckbox v-model="formData.agreement">
                {{ $t('register.agreeText') }}
                <router-link
                  style="color: var(--main-color); text-decoration: none"
                  to="/privacy-policy"
                  >{{ $t('register.privacyPolicy') }}</router-link
                >
              </ElCheckbox>
            </ElFormItem>

            <div style="margin-top: 15px">
              <ElButton
                class="register-btn"
                type="primary"
                @click="register"
                :loading="loading"
                v-ripple
              >
                {{ $t('register.submitBtnText') }}
              </ElButton>
            </div>

            <div class="footer">
              <p>
                {{ $t('register.hasAccount') }}
                <router-link :to="RoutesAlias.Login">{{ $t('register.toLogin') }}</router-link>
              </p>
            </div>
          </ElForm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import AppConfig from '@/config'
  import { RoutesAlias } from '@/router/routesAlias'
  import type { FormInstance, FormRules } from 'element-plus'
  import { useI18n } from 'vue-i18n'
  import ArtLogo from '@/components/core/base/art-logo/index.vue'
  import { fetchSendVerificationCode, fetchRegister } from '@/api/auth'
  
  defineOptions({ name: 'Register' })

  const { t } = useI18n()

  const router = useRouter()
  const formRef = ref<FormInstance>()

  const systemName = AppConfig.systemInfo.name
  const loading = ref(false)
  const countdown = ref(0)

  let countdownTimer: number | null = null

  const formData = reactive({
    email: '',
    code: '',
    username: '',
    password: '',
    confirmPassword: '',
    agreement: false
  })

  const validatePass = (rule: any, value: string, callback: any) => {
    if (value === '') {
      callback(new Error(t('register.placeholder[5]')))
    } else {
      if (formData.confirmPassword !== '') {
        formRef.value?.validateField('confirmPassword')
      }
      callback()
    }
  }

  const validatePass2 = (rule: any, value: string, callback: any) => {
    if (value === '') {
      callback(new Error(t('register.rule[0]')))
    } else if (value !== formData.password) {
      callback(new Error(t('register.rule[1]')))
    } else {
      callback()
    }
  }

  const rules = reactive<FormRules>({
    email: [
      { required: true, message: t('register.placeholder[0]'), trigger: 'blur' },
      { min: 3, max: 50, message: t('register.rule[2]'), trigger: 'blur' }
    ],
    username: [
      { required: true, message: t('register.placeholder[4]'), trigger: 'blur' },
      { min: 3, max: 20, message: t('register.rule[2]'), trigger: 'blur' }
    ],
    password: [
      { required: true, validator: validatePass, trigger: 'blur' },
      { min: 6, message: t('register.rule[3]'), trigger: 'blur' }
    ],
    confirmPassword: [{ required: true, validator: validatePass2, trigger: 'blur' }],
    agreement: [
      {
        validator: (rule: any, value: boolean, callback: any) => {
          if (!value) {
            callback(new Error(t('register.rule[4]')))
          } else {
            callback()
          }
        },
        trigger: 'change'
      }
    ]
  })

  // 然后修改register函数
  const register = async () => {
    if (!formRef.value) return
  
    try {
      await formRef.value.validate()
      loading.value = true
  
      // 调用实际的注册API
      await fetchRegister({
        email: formData.email,
        code: formData.code,
        username: formData.username,
        password: formData.password
      })
  
      loading.value = false
      ElMessage.success(t('register.placeholder[7]'))
      toLogin()
    } catch (error) {
      loading.value = false
      console.log(t('register.placeholder[8]'), error)
    }
  }

  // 发送验证码
  const sendVerificationCode = async () => {
    // 先验证邮箱
    try {
      await formRef.value?.validateField('email')
      
      // 调用API发送验证码
      loading.value = true
      await fetchSendVerificationCode({ email: formData.email })
      
      loading.value = false
      ElMessage.success(t('code.placeholder[0]'))
      startCountdown()
    } catch (error) {
      loading.value = false
      console.log(t('code.placeholder[1]'), error)
    }
  }

  // 开始倒计时
  const startCountdown = () => {
    countdown.value = 60
    
    if (countdownTimer) {
      clearInterval(countdownTimer)
    }
    
    countdownTimer = window.setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        if (countdownTimer) {
          clearInterval(countdownTimer)
          countdownTimer = null
        }
      }
    }, 1000)
  }

  const toLogin = () => {
    setTimeout(() => {
      router.push(RoutesAlias.Login)
    }, 1000)
  }
</script>

<style lang="scss" scoped>
  @use '../login/index' as login;
  @use './index' as register;
</style>
