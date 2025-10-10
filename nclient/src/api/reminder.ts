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

/** 更新项目 */
export function fetchUpdateProject(params: Api.Reminder.UpdateProjectParams) {
  return request.post<void>({
    url: '/api/reminder/projects/update',
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

/** 交换位置*/
export function fetchSwapPositionProject(params: Api.Reminder.SwapPositionProjectParams) {
  return request.post<void>({
    url: '/api/reminder/projects/swap-position',
    data: params,
    showSuccessMessage: false
  })
}
