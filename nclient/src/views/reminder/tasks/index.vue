<template>
  <div class="art-full-height">
    <div class="tree-container">
      <!-- 左侧拖拽部分 -->
      <div class="left-sidebar">
        <ProjectSidebar />
      </div>

      <!-- 右侧表格部分 -->
      <div class="right-content art-full-height">
        <TaskTable />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  defineOptions({ name: 'Tasks' })
  import ProjectSidebar from './widget/ProjectSidebar.vue'
  import TaskTable from './widget/TaskTable.vue'
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