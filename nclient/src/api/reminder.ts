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

/**
 * 获取用户所有项目
 * @returns 用户所有项目
 */
export function fetchGetAllProjects() {
  return request.get<Api.Reminder.GetAllProjectsResponse[]>({
    url: '/api/reminder/projects/get-all',
    showSuccessMessage: false
  })
}
