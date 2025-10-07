<template>
  <div class="blank-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>空白页</span>
        </div>
      </template>
      <div class="content">
        <p>此页面为空白页面，等待后续功能开发。</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
  defineOptions({ name: 'ReminderBlank' })
</script>

<style lang="scss" scoped>
  .blank-container {
    padding: 20px;
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .content {
      text-align: center;
      padding: 40px 0;
      color: #606266;
    }
  }
</style>