/**
 * namespace: Api
 *
 * 所有接口相关类型定义
 * 在.vue文件使用会报错，需要在 eslint.config.mjs 中配置 globals: { Api: 'readonly' }
 */

declare namespace Api {
  /** 通用类型 */
  namespace Common {
    /** 分页参数 */
    interface PaginationParams {
      /** 当前页码 */
      current: number
      /** 每页条数 */
      size: number
      /** 总条数 */
      total: number
    }

    /** 通用搜索参数 */
    type CommonSearchParams = Pick<PaginationParams, 'current' | 'size'>

    /** 分页响应基础结构 */
    interface PaginatedResponse<T = any> {
      records: T[]
      current: number
      size: number
      total: number
    }

    /** 启用状态 */
    type EnableStatus = '1' | '2'
  }

  /** 认证类型 */
  namespace Auth {
    /** 登录参数 */
    interface LoginParams {
      email: string
      password: string
    }

    /** 登录响应 */
    interface LoginResponse {
      token: string
      refreshToken: string
    }

    /** 用户信息 */
    interface UserInfo {
      // buttons: string[]
      // roles: string[]
      userId: number
      userName: string
      email: string
      avatar?: string
    }

    /** 发送验证码参数 */
    interface SendVerificationCodeParams {
      email: string
    }

    /** 注册参数 */
    interface RegisterParams {
      email: string
      username: string
      password: string
      code: string
    }
  }

  /** 提醒类型 */
  namespace Reminder {
    /** 创建项目参数 */
    interface CreateProjectParams {
      name: string
      description?: string
      color?: string
      icon?: string
    }

    /** 更新项目参数 */
    interface UpdateProjectParams {
      projectId: number
      name: string
      description?: string
      color?: string
      icon?: string
    }

    /** 交换位置 */
    interface BatchUpdatePositionParams {
      projects: Array<{
        projectId: number
        sortOrder: number
      }>
    }

    /** 获取所有项目响应 */
    interface GetAllProjectsResponse {
      id: number
      projectId: number
      name: string
      description?: string
      color?: string
      icon?: string
      userId: number
      sortOrder?: number
      isArchived?: boolean
    }

    /** 创建任务参数 */
    interface CreateTaskParams {
      projectId?: number
      title: string
      category: string
      parentTaskId?: number
      description?: string
      dueDate?: string
      startDate?: string
      reminderSentAt?: string
      priority?: string
    }
  }

  /** 系统管理类型 */
  namespace SystemManage {
    /** 用户列表 */
    type UserList = Api.Common.PaginatedResponse<UserListItem>

    /** 用户列表项 */
    interface UserListItem {
      id: number
      avatar: string
      status: string
      userName: string
      userGender: string
      nickName: string
      userPhone: string
      userEmail: string
      userRoles: string[]
      createBy: string
      createTime: string
      updateBy: string
      updateTime: string
    }

    /** 用户搜索参数 */
    type UserSearchParams = Partial<
      Pick<UserListItem, 'id' | 'userName' | 'userGender' | 'userPhone' | 'userEmail' | 'status'> &
        Api.Common.CommonSearchParams
    >

    /** 角色列表 */
    type RoleList = Api.Common.PaginatedResponse<RoleListItem>

    /** 角色列表项 */
    interface RoleListItem {
      roleId: number
      roleName: string
      roleCode: string
      description: string
      enabled: boolean
      createTime: string
    }

    /** 角色搜索参数 */
    type RoleSearchParams = Partial<
      Pick<RoleListItem, 'roleId' | 'roleName' | 'roleCode' | 'description' | 'enabled'> &
        Api.Common.CommonSearchParams
    >
  }
}
