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

            <div class="form-group">
              <label for="useremail">Email</label>
              <input v-model="form.email" type="email" class="form-control" placeholder="Enter email">
            </div>

            <div class="form-group">
              <label for="code">Validation Code</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input v-model="form.code" type="text" class="form-control" placeholder="Validation Code">
                </div>
                <div class="col-md-4 col-4">
                  <button class="btn btn-primary btn-block" @click="requestCode">Send</button>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="username">Username</label>
              <input v-model="form.username" type="text" class="form-control" placeholder="Enter username">
            </div>

            <div class="form-group">
              <label for="userpassword">Password</label>
              <div class="row">
                <div class="col-md-8 col-8">
                  <input v-model="form.password" type="password" class="form-control" placeholder="Enter password">
                </div>
                <div class="col-md-4 col-4">
                  <button class="btn btn-primary w-md waves-effect waves-light" @click="handleRegister">Register</button>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-4 text-center">
              <p>Already have an account ? <router-link to="/auth/login" class="font-weight-medium text-primary">Login</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  data() {
    return {
      form: {
        email: '',
        code: '',
        username: '',
        password: ''
      }
    }
  },
  methods: {
    requestCode() {
      // 发送验证码逻辑
    },
    handleRegister() {
      // 注册逻辑
    }
  }
}
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>