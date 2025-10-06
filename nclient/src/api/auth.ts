import request from '@/utils/http'

/**
 * 登录
 * @param params 登录参数
 * @returns 登录响应
 */
export function fetchLogin(params: Api.Auth.LoginParams) {
  return request.post<Api.Auth.LoginResponse>({
    url: '/api/auth/login',
    data: params
    // showSuccessMessage: true // 显示成功消息
    // showErrorMessage: false // 不显示错误消息
  })
}

/**
 * 获取用户信息
 * @returns 用户信息
 */
export function fetchGetUserInfo() {
  return request.get<Api.Auth.UserInfo>({
    url: '/api/auth/profile'
    // 自定义请求头
    // headers: {
    //   'X-Custom-Header': 'your-custom-value'
    // }
  })
}

/**
 * 发送验证码
 * @param params 验证码参数
 * @returns 发送验证码响应
 */
export function fetchSendVerificationCode(params: Api.Auth.SendVerificationCodeParams) {
  return request.post<void>({
    url: '/api/auth/send-code',
    data: params,
    showSuccessMessage: false
  })
}

/**
 * 用户注册
 * @param params 注册参数
 * @returns 注册响应
 */
export function fetchRegister(params: Api.Auth.RegisterParams) {
  return request.post<void>({
    url: '/api/auth/register',
    data: params,
    showSuccessMessage: false
  })
}
