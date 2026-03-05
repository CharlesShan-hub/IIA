<template>
  <ElCard class="art-table-card" shadow="never" style="margin-top: 0; height: 100%">
    <!-- 表格头部 -->
    <div
      class="table-header"
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
      "
    >
      <h3 style="margin: 0">任务列表</h3>
      <div>
        <ElButton @click="toggleExpand" v-ripple>
          {{ isExpanded ? '收起' : '展开' }}
        </ElButton>
        <ElButton type="primary" v-ripple @click="showAddTaskDialog"> 添加任务 </ElButton>
      </div>
    </div>

    <ArtTable
      ref="tableRef"
      rowKey="id"
      :loading="loading"
      :columns="columns"
      :data="filteredTableData"
      :stripe="false"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      :default-expand-all="false"
    />
  </ElCard>

  <!-- 任务添加弹窗 -->
  <ElDialog v-model="dialogVisible" title="添加任务" width="500px" @closed="resetForm">
    <ElForm :model="taskForm" label-width="80px" ref="taskFormRef">
      <ElFormItem label="任务名称" prop="title" required>
        <ElInput v-model="taskForm.title" placeholder="请输入任务名称" />
      </ElFormItem>
      <ElFormItem label="所属项目" prop="projectId">
        <ElSelect v-model="taskForm.projectId" placeholder="请选择所属项目" style="width: 100%">
          <ElOption value="" label="无项目" />
          <ElOption
            v-for="project in availableProjects"
            :key="project.id"
            :label="project.name"
            :value="project.id"
          />
        </ElSelect>
      </ElFormItem>
      <ElFormItem label="任务分类" prop="category">
        <ElInput v-model="taskForm.category" placeholder="请输入任务分类" />
      </ElFormItem>
      <ElFormItem label="父任务" prop="parentTaskId">
        <ElSelect v-model="taskForm.parentTaskId" placeholder="请选择父任务" style="width: 100%">
          <ElOption value="" label="无父任务" />
          <ElOption
            v-for="task in parentTasks"
            :key="task.id"
            :label="task.title"
            :value="task.id"
          />
        </ElSelect>
      </ElFormItem>
      <ElFormItem label="任务描述" prop="description">
        <ElInput
          v-model="taskForm.description"
          type="textarea"
          placeholder="请输入任务描述（可选）"
        />
      </ElFormItem>
      <ElFormItem label="开始日期" prop="startDate">
        <ElDatePicker
          v-model="taskForm.startDate"
          type="date"
          placeholder="请选择开始日期"
          style="width: 100%"
        />
      </ElFormItem>
      <ElFormItem label="截止日期" prop="dueDate">
        <ElDatePicker
          v-model="taskForm.dueDate"
          type="date"
          placeholder="请选择截止日期"
          style="width: 100%"
        />
      </ElFormItem>
      <ElFormItem label="优先级" prop="priority">
        <ElSelect v-model="taskForm.priority" placeholder="请选择优先级" style="width: 100%">
          <ElOption value="low" label="低" />
          <ElOption value="medium" label="中" />
          <ElOption value="high" label="高" />
        </ElSelect>
      </ElFormItem>
    </ElForm>
    <template #footer>
      <span class="dialog-footer">
        <ElButton @click="dialogVisible = false"> 取消 </ElButton>
        <ElButton type="primary" @click="handleSaveTask"> 确定 </ElButton>
      </span>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
  defineOptions({ name: 'TaskTable' })

  // 导入必要的组件和函数
  import { ref, computed, onMounted, nextTick, h } from 'vue'
  import {
    ElButton,
    ElMessage,
    ElTag,
    ElDialog,
    ElForm,
    ElFormItem,
    ElInput,
    ElSelect,
    ElOption,
    ElDatePicker
  } from 'element-plus'
  import ArtTable from '@/components/core/tables/art-table/index.vue'
  import { useTableColumns } from '@/composables/useTableColumns'
  import { fetchGetAllProjects } from '@/api/reminder'

  // 任务类型定义
  interface Task {
    id: number
    title: string
    description?: string
    status: 'pending' | 'completed' | 'in_progress'
    priority: 'low' | 'medium' | 'high'
    dueDate?: string
    startDate?: string
    projectId?: number
    category?: string
    parentTaskId?: number
    children?: Task[]
  }

  // 项目类型定义
  interface Project {
    id: number
    name: string
  }

  // 表格相关状态
  const loading = ref(false)
  const isExpanded = ref(false)
  const tableRef = ref()
  const tableData = ref<Task[]>([])

  // 弹窗相关状态
  const dialogVisible = ref(false)
  const taskFormRef = ref()
  const availableProjects = ref<Project[]>([])
  const taskForm = ref<Api.Reminder.CreateTaskParams>({
    projectId: undefined,
    title: '',
    category: '',
    parentTaskId: undefined,
    description: '',
    dueDate: undefined,
    startDate: undefined,
    reminderSentAt: undefined,
    priority: 'medium'
  })

  // 过滤出可作为父任务的任务列表
  const parentTasks = computed(() => {
    // 这里可以根据实际需求过滤任务
    return tableData.value.filter((task) => !task.parentTaskId)
  })

  // 表格列配置
  const { columnChecks, columns } = useTableColumns(() => [
    {
      prop: 'title',
      label: '任务名称',
      minWidth: 180
    },
    {
      prop: 'projectId',
      label: '所属项目',
      minWidth: 120,
      formatter: (row: Task) => {
        const project = availableProjects.value.find(p => p.id === row.projectId)
        return project?.name || '无项目'
      }
    },
    {
      prop: 'category',
      label: '任务分类',
      minWidth: 100,
      formatter: (row: Task) => row.category || '无'
    },
    {
      prop: 'parentTaskId',
      label: '父任务',
      minWidth: 150,
      formatter: (row: Task) => {
        if (!row.parentTaskId) return '无'
        // 递归查找父任务名称
        const findParentTask = (tasks: Task[], id: number): string => {
          for (const task of tasks) {
            if (task.id === id) return task.title
            if (task.children) {
              const found = findParentTask(task.children, id)
              if (found) return found
            }
          }
          return '未知'
        }
        return findParentTask(tableData.value, row.parentTaskId)
      }
    },
    {
      prop: 'status',
      label: '状态',
      formatter: (row: Task) => {
        const statusMap: Record<string, { type: string; text: string }> = {
          pending: { type: 'warning', text: '待处理' },
          in_progress: { type: 'primary', text: '进行中' },
          completed: { type: 'success', text: '已完成' }
        }
        const status = statusMap[row.status] || { type: 'info', text: '未知' }
        return h(ElTag, { type: status.type }, () => status.text)
      }
    },
    {
      prop: 'priority',
      label: '优先级',
      formatter: (row: Task) => {
        const priorityMap: Record<string, { type: string; text: string }> = {
          low: { type: 'success', text: '低' },
          medium: { type: 'warning', text: '中' },
          high: { type: 'danger', text: '高' }
        }
        const priority = priorityMap[row.priority] || { type: 'info', text: '未知' }
        return h(ElTag, { type: priority.type }, () => priority.text)
      }
    },
    {
      prop: 'startDate',
      label: '开始日期',
      minWidth: 120,
      formatter: (row: Task) => row.startDate || '无'
    },
    {
      prop: 'dueDate',
      label: '截止日期',
      minWidth: 120,
      formatter: (row: Task) => row.dueDate || '无'
    },
    {
      prop: 'description',
      label: '任务描述',
      minWidth: 200,
      formatter: (row: Task) => row.description || '无'
    },
    {
      prop: 'operation',
      label: '操作',
      width: 160, // 增加宽度以容纳水平排列的按钮
      align: 'center', // 居中对齐
      formatter: (row: Task) => {
        return h('div', { style: 'display: flex; gap: 8px; justify-content: center;' }, [
          h(ElButton, { size: 'small', type: 'primary' }, () => '编辑'),
          h(ElButton, { size: 'small', type: 'danger' }, () => '删除')
        ])
      }
    }
  ])

  // 过滤后的表格数据
  const filteredTableData = computed(() => {
    // 在实际应用中，这里可以根据搜索条件过滤数据
    return tableData.value
  })

  // 加载任务数据
  const loadTasks = async () => {
    loading.value = true
    try {
      // 模拟API请求延迟
      await new Promise((resolve) => setTimeout(resolve, 500))

      // 模拟任务数据
      tableData.value = [
        {
          id: 1,
          title: '项目规划文档',
          description: '制定详细的项目规划和时间表',
          status: 'in_progress',
          priority: 'high',
          startDate: '2023-12-01',
          dueDate: '2023-12-31',
          category: '项目管理',
          children: [
            {
              id: 11,
              title: '需求分析',
              description: '分析用户需求并撰写需求文档',
              status: 'completed',
              priority: 'medium',
              startDate: '2023-12-01',
              dueDate: '2023-12-10',
              category: '需求',
              parentTaskId: 1
            },
            {
              id: 12,
              title: '技术选型',
              description: '评估和选择合适的技术栈',
              status: 'in_progress',
              priority: 'medium',
              startDate: '2023-12-11',
              dueDate: '2023-12-15',
              category: '技术',
              parentTaskId: 1
            }
          ]
        },
        {
          id: 2,
          title: 'UI设计稿',
          description: '设计应用的用户界面原型',
          status: 'pending',
          priority: 'medium',
          startDate: '2023-12-20',
          dueDate: '2024-01-15',
          category: '设计',
          children: [
            {
              id: 21,
              title: '登录页面',
              description: '设计用户登录和注册页面',
              status: 'pending',
              priority: 'low',
              startDate: '2023-12-20',
              dueDate: '2024-01-05',
              category: '界面',
              parentTaskId: 2
            },
            {
              id: 22,
              title: '仪表盘',
              description: '设计数据仪表盘界面',
              status: 'pending',
              priority: 'medium',
              startDate: '2024-01-06',
              dueDate: '2024-01-10',
              category: '界面',
              parentTaskId: 2
            }
          ]
        },
        {
          id: 3,
          title: '数据库设计',
          description: '设计系统的数据库结构',
          status: 'completed',
          priority: 'high',
          startDate: '2023-12-10',
          dueDate: '2023-12-20',
          category: '技术'
        }
      ]
    } catch (error) {
      ElMessage.error('获取任务列表失败')
      console.error('获取任务列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 加载项目列表
  const loadProjects = async () => {
    try {
      const response = await fetchGetAllProjects()
      availableProjects.value = response.map((project) => ({
        id: project.projectId,
        name: project.name
      }))
    } catch (error) {
      console.error('获取项目列表失败:', error)
    }
  }

  // 展开/收起功能
  const toggleExpand = () => {
    isExpanded.value = !isExpanded.value
    nextTick(() => {
      if (tableRef.value?.elTableRef && filteredTableData.value) {
        const processRows = (rows: any[]) => {
          rows.forEach((row) => {
            if (row.children?.length) {
              tableRef.value.elTableRef.toggleRowExpansion(row, isExpanded.value)
              processRows(row.children)
            }
          })
        }
        processRows(filteredTableData.value)
      }
    })
  }

  // 显示添加任务弹窗
  const showAddTaskDialog = () => {
    loadProjects() // 打开弹窗时加载项目列表
    dialogVisible.value = true
  }

  // 重置表单
  const resetForm = () => {
    taskForm.value = {
      projectId: undefined,
      title: '',
      category: '',
      parentTaskId: undefined,
      description: '',
      dueDate: undefined,
      startDate: undefined,
      reminderSentAt: undefined,
      priority: 'medium'
    }
    // 重置表单验证状态
    if (taskFormRef.value) {
      taskFormRef.value.resetFields()
    }
  }

  // 保存任务
  const handleSaveTask = async () => {
    // 表单验证
    if (!taskForm.value.title.trim()) {
      ElMessage.error('请输入任务名称')
      return
    }

    try {
      loading.value = true
      // 模拟API请求延迟
      await new Promise((resolve) => setTimeout(resolve, 500))

      // 生成新任务ID（实际应用中应由后端生成）
      const newTaskId = Math.max(...tableData.value.map((task) => task.id), 0) + 1

      // 创建新任务对象
      const newTask: Task = {
        id: newTaskId,
        title: taskForm.value.title.trim(),
        description: taskForm.value.description || '',
        status: 'pending',
        priority: (taskForm.value.priority as 'low' | 'medium' | 'high') || 'medium',
        dueDate: taskForm.value.dueDate,
        projectId: taskForm.value.projectId
      }

      // 根据是否有父任务决定添加位置
      if (taskForm.value.parentTaskId) {
        const parentTask = tableData.value.find((task) => task.id === taskForm.value.parentTaskId)
        if (parentTask) {
          if (!parentTask.children) {
            parentTask.children = []
          }
          parentTask.children.push(newTask)
        } else {
          tableData.value.unshift(newTask)
        }
      } else {
        tableData.value.unshift(newTask)
      }

      // 显示成功消息
      ElMessage.success('任务创建成功')
      dialogVisible.value = false
      resetForm()
    } catch (error) {
      ElMessage.error('任务创建失败')
      console.error('任务创建失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 组件挂载时加载任务列表
  onMounted(() => {
    loadTasks()
  })
</script>

<style lang="scss" scoped>
  // 为表格操作按钮添加自定义样式
  :deep(.el-table .cell .el-button--) {
    margin: 0 !important;
  }
</style>
