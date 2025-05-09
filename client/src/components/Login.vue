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

            <div class="form-group">
              <label for="mail">Mail</label>
              <input v-model="form.mail" type="text" class="form-control" placeholder="Mail">
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input v-model="form.password" type="password" class="form-control" placeholder="Password">
            </div>

            <div class="form-group row">
              <div class="col-sm-6">
                <div class="custom-control custom-checkbox">
                  <input v-model="form.remember" type="checkbox" class="custom-control-input" id="remember">
                  <label class="custom-control-label" for="remember">Remember me</label>
                </div>
              </div>
              <div class="col-sm-6 text-right">
                <button @click="handleLogin" class="btn btn-primary w-md waves-effect waves-light">Log In</button>
              </div>
            </div>

            <div class="form-group mt-2 mb-0 row">
              <div class="col-12 mt-3">
                <router-link to="/auth/forgot-password"><i class="mdi mdi-lock"></i> Forgot your password?</router-link>
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
  name: 'LoginPage',
  data() {
    return {
      // 移除backgroundStyle数据项
      form: {
        mail: '',
        password: '',
        remember: false
      }
    }
  },
  methods: {
    // async handleLogin() {
    //   try {
    //     // 这里替换为实际的登录API调用
    //     const response = await fetch('/api/login', {
    //       method: 'POST',
    //       body: JSON.stringify(this.form)
    //     })
    //     // 处理登录结果...
    //   } catch (error) {
    //     console.error('Login failed:', error)
    //   }
    // }
  }
}
</script>