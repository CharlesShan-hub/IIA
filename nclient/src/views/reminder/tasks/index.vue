<template>
  <div class="art-full-height">
    <div class="tree-container">
      <div class="left-sidebar">
        <ElCard class="art-table-card" shadow="never" style="margin-top: 0">
          <!-- 第一组拖拽项：今天和收集箱 -->
          <el-divider>
            <el-icon><star-filled /></el-icon>
          </el-divider>
          <div class="section-title">{{ $t('tasks.project.title[0]') }}</div>
          <VueDraggable v-model="dragItems">
            <div class="drag-item" v-for="item in dragItems" :key="item.id">
              {{ item.name }}
            </div>
          </VueDraggable>

          <!-- 第二组拖拽项：Projects -->
          <el-divider>
            <el-icon><star-filled /></el-icon>
          </el-divider>
          <div class="section-header">
            <div class="section-title">{{ $t('tasks.project.title[1]') }}</div>
            <div class="section-icon">
              <i class="iconfont-sys" @click="showAddProjectDialog">&#xe83e;</i>
            </div>
          </div>
          <VueDraggable v-model="projects" @end="handleProjectDragEnd">
            <div class="drag-item" v-for="project in projects" :key="project.id" @click="showEditProjectDialog(project)">
              <i v-if="project.icon" :class="`iconfont-sys ${project.icon}`" style="margin-right: 8px; display: inline-block; width: 20px; height: 20px;"></i>
              <span>{{ project.name }}</span>
            </div>
          </VueDraggable>
        </ElCard>
      </div>

      <div class="right-content art-full-height">
        <!-- 搜索栏占位-->
      </div>
    </div>
  </div>

  <!-- 项目编辑弹窗 -->
  <ElDialog v-model="dialogVisible" :title="dialogTitle" width="500px" @closed="resetForm">
    <ElForm :model="projectForm" label-width="80px">
      <ElFormItem label="项目名称" required>
        <ElInput v-model="projectForm.name" placeholder="请输入项目名称" />
      </ElFormItem>
      <ElFormItem label="项目描述">
        <ElInput v-model="projectForm.description" type="textarea" placeholder="请输入项目描述（可选）" />
      </ElFormItem>
      <ElFormItem label="项目颜色">
        <ElColorPicker v-model="projectForm.color" :predefine="predefineColors" show-alpha />
      </ElFormItem>
      <ElFormItem label="项目图标">
        <ArtIconSelector v-model="projectForm.icon" :iconType="IconTypeEnum.CLASS_NAME" />
      </ElFormItem>
    </ElForm>
    <template #footer>
      <span class="dialog-footer">
        <ElButton v-if="isEditing" type="danger" @click="handleDeleteProject"> 删除 </ElButton>
        <ElButton type="primary" @click="handleSaveProject">
          {{ isEditing ? '更新' : '添加' }}
        </ElButton>
      </span>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
  defineOptions({ name: 'Tasks' })

  import { VueDraggable } from 'vue-draggable-plus'
  import { ref, computed, onMounted } from 'vue'
  import { StarFilled } from '@element-plus/icons-vue'
  import { ElDialog, ElForm, ElFormItem, ElInput, ElButton, ElMessage, ElMessageBox, ElColorPicker } from 'element-plus'
  import { IconTypeEnum } from '@/enums/appEnum'
  
  // 导入API函数
  import { fetchCreateProject, fetchGetAllProjects, fetchUpdateProject, fetchSwapPositionProject } from '@/api/reminder'
  
  // 项目类型定义
  interface Project {
    id: number
    name: string
    description?: string
    color?: string
    icon?: string
  }
  
  // 导入useI18n钩子
  import { useI18n } from 'vue-i18n'
  
  // 然后在组件中使用
  const { t } = useI18n()
  
  // 现在您可以在JS代码中使用t()函数进行翻译
  const dragItems = ref([
    { id: 1, name: t('tasks.project.title[2]') },
    { id: 2, name: t('tasks.project.title[3]') }
  ])
  
  // 如果您需要在其他函数中使用翻译
  const someFunction = () => {
    const translatedText = t('some.key')
    console.log(translatedText)
  }

  // 第二组拖拽项：Projects
  const projects = ref<Project[]>([])

  // 预定义颜色
  const predefineColors = [
    '#409EFF',
    '#67C23A',
    '#E6A23C',
    '#F56C6C',
    '#909399',
    '#722ED1',
    '#13C2C2',
    '#FFB74D',
    '#F06292',
    '#4DB6AC'
  ]

  // 弹窗状态管理
  const dialogVisible = ref(false)
  const dialogTitle = ref('添加项目')
  const editingProjectIndex = ref<number>(-1)
  const projectForm = ref<Project>({
    id: 0,
    name: '',
    description: '',
    color: '#409EFF',
    icon: ''
  })

  // 计算属性
  const isEditing = computed(() => editingProjectIndex.value >= 0)

  // 加载项目列表
  const loadProjects = async () => {
    try {
      const response = await fetchGetAllProjects()
      // 将API返回的项目数据映射到本地Project接口格式
      projects.value = response.map(project => ({
        id: project.projectId,
        name: project.name,
        description: project.description || '',
        color: project.color || '#409EFF',
        icon: project.icon || ''
      }))
    } catch (error) {
      ElMessage.error('获取项目列表失败')
      console.error('获取项目列表失败:', error)
    }
  }

  // 重置表单
  const resetForm = () => {
    projectForm.value = {
      id: 0,
      name: '',
      description: '',
      color: '#409EFF',
      icon: ''
    }
    editingProjectIndex.value = -1
  }

  // 显示添加项目弹窗
  const showAddProjectDialog = () => {
    dialogTitle.value = '添加项目'
    projectForm.value = {
      id: 0,
      name: '',
      description: '',
      color: '#409EFF',
      icon: ''
    }
    editingProjectIndex.value = -1
    dialogVisible.value = true
  }

  // 显示编辑项目弹窗
  const showEditProjectDialog = (project: Project) => {
    dialogTitle.value = '编辑项目'
    projectForm.value = { ...project }
    editingProjectIndex.value = projects.value.findIndex(
      (p) => p.id === project.id
    )
    dialogVisible.value = true
  }

  // 保存项目
  const handleSaveProject = async () => {
    if (!projectForm.value.name.trim()) {
      ElMessage.error('请输入项目名称')
      return
    }

    if (isEditing.value) {
      // 更新现有项目
      try {
        // 准备更新项目参数
        const updateParams: Api.Reminder.UpdateProjectParams = {
          projectId: projectForm.value.id,
          name: projectForm.value.name.trim(),
          description: projectForm.value.description.trim() || undefined,
          color: projectForm.value.color || '#409EFF',
          icon: projectForm.value.icon || undefined
        }
        
        // 调用更新项目API
        await fetchUpdateProject(updateParams)
        
        // 重新获取项目列表，确保数据最新
        await loadProjects()
        ElMessage.success('项目更新成功')
        dialogVisible.value = false
        resetForm()
      } catch (error) {
        ElMessage.error('项目更新失败，请重试')
        console.error('更新项目失败:', error)
        return
      }
    } else {
      // 添加新项目
      try {
        // 准备创建项目参数
        const createParams: Api.Reminder.CreateProjectParams = {
          name: projectForm.value.name.trim(),
          description: projectForm.value.description.trim() || undefined,
          color: projectForm.value.color || '#409EFF',
          icon: projectForm.value.icon || undefined
        }
        
        // 调用创建项目API
        await fetchCreateProject(createParams)
        
        // 重新获取项目列表，确保数据最新
        await loadProjects()
        ElMessage.success('项目添加成功')
        dialogVisible.value = false
        resetForm()
      } catch (error) {
        ElMessage.error('项目添加失败，请重试')
        console.error('创建项目失败:', error)
        return
      }
    }
  }

  // 删除项目
  const handleDeleteProject = () => {
    if (isEditing.value) {
      ElMessageBox.confirm('确定要删除这个项目吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        projects.value.splice(editingProjectIndex.value, 1)
        dialogVisible.value = false
        resetForm()
        ElMessage.success('项目已删除')
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
  }
  
  // 组件挂载时加载项目列表
  onMounted(() => {
    loadProjects()
  })

  // 处理项目拖拽结束事件
  const handleProjectDragEnd = async () => {
    try {
      // 记录开始时间，用于性能监控
      const startTime = Date.now()
      console.log('拖拽结束，开始更新所有项目位置')
      
      // 创建一个数组来保存所有更新请求
      const updatePromises = projects.value.map(async (project, index) => {
        // 位置从1开始
        const newSortOrder = index + 1
        
        // 构建更新位置的参数
        const swapPositionParams: Api.Reminder.SwapPositionProjectParams = {
          projectId: project.id,
          sortOrder: newSortOrder
        }
        
        console.log(`正在更新项目ID: ${project.id}，新位置: ${newSortOrder}`)
        
        // 调用API更新位置
        return fetchSwapPositionProject(swapPositionParams)
      })
      
      // 等待所有位置更新请求完成
      await Promise.all(updatePromises)
      
      // 重新获取项目列表，确保前端显示与后端一致
      await loadProjects()
      
      // 计算总耗时
      const endTime = Date.now()
      console.log(`所有项目位置更新完成，耗时: ${endTime - startTime}ms`)
      // ElMessage.success('项目排序已更新')
    } catch (error) {
      console.error('更新项目位置失败:', error)
      ElMessage.error('项目排序更新失败')
      // 失败时重新加载列表以恢复状态
      await loadProjects()
    }
  }
</script>

<style lang="scss" scoped>
  .tree-container {
    box-sizing: border-box;
    display: flex;
    gap: 16px;
    height: 100%;

    .left-sidebar {
      flex-shrink: 0;
      width: 230px;
      height: 100%;
    }

    .right-content {
      flex-grow: 1;
      min-width: 0;
      height: 100%;
    }

    .art-table-card {
      display: flex;
      flex-direction: column;
      height: 100%;
      padding: 16px;
    }
  }

  .drag-item {
    padding: 10px;
    margin-bottom: 10px;
    cursor: move;
    background-color: rgba(var(--art-gray-200-rgb), 0.8);
    border-radius: 4px;
  }

  .divider {
    height: 1px;
    background-color: #e5e5e5;
    margin: 20px 0;
  }

  .section-title {
    font-weight: bold;
    margin-bottom: 10px;
    color: #606266;
    font-size: 14px;
    line-height: 20px;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }

  .section-icon {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    height: 20px;
  }

  .section-icon i {
    font-size: 16px;
    color: var(--art-gray-500);
    cursor: pointer;
    line-height: 20px;
  }

  @media screen and (max-width: $device-ipad) {
    .tree-container {
      display: block;
      gap: 0;
      height: auto;

      .left-sidebar {
        width: 100%;
        height: auto;
        margin-bottom: 20px;
      }
    }
  }
</style>