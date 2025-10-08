import request from '@/utils/http'

/**
 * 添加项目
 * @param params 添加项目参数
 * @returns 添加项目响应
 */
export function fetchCreateProject(params: Api.Reminder.CreateProjectParams) {
  return request.post<void>({
    url: '/api/reminder/projects/create',
    data: params,
    showSuccessMessage: false
  })
}