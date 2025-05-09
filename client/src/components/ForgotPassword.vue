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

            <div class="form-group">
              <label for="useremail">Email</label>
              <input v-model="form.email" type="email" class="form-control" placeholder="Enter email">
            </div>

            <div class="form-group">
              <label for="useremail">Verification code</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input v-model="form.code" type="text" class="form-control" placeholder="Enter Verification Code">
                </div>
                <div class="col-md-4 col-4">
                  <button class="btn btn-primary btn-block" @click="sendCode">Send</button>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="useremail">New Password</label>
              <input v-model="form.newPassword" type="password" class="form-control" placeholder="New Password">
            </div>

            <div class="form-group">
              <label for="useremail">New Password Again</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input v-model="form.confirmPassword" type="password" class="form-control" placeholder="New Password Again">
                </div>
                <div class="col-md-4 col-4">
                  <button class="btn btn-primary btn-block" @click="resetPassword">Reset</button>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-4 text-center">
              <p>Don't have an account ? <router-link to="/auth/register" class="font-weight-medium text-primary">Signup now</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ForgotPasswordPage',
  data() {
    return {
      form: {
        email: '',
        code: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    sendCode() {
      // 发送验证码逻辑
    },
    resetPassword() {
      // 重置密码逻辑
    }
  }
}
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>