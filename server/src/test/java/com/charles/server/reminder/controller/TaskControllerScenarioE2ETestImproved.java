package com.charles.server.reminder.controller;

import com.charles.server.BaseE2eDatabaseTest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 改进的场景测试，使用BaseE2eDatabaseTest的基础函数
 */
class TaskControllerScenarioE2ETestImproved extends BaseE2eDatabaseTest {
    @Test
    void create_project() throws Exception {
        // 创建项目
        Long projectId = createProject("P1");
        assertNotNull(projectId);
    }
    @Test
    void create_root_task() throws Exception {
        // 创建根任务
        Long taskId = createRootTask(null, "T1");
        assertNotNull(taskId);
    }
    
    @Test
    void scenario_createProject_then_twoRootTasks_then_oneSubTask() throws Exception {
        // 1. 创建项目
        Long projectId = createProject("Default");
        
        // 2. 创建两个根任务
        Long task1Id = createRootTask(projectId, "T1");
        Long task2Id = createRootTask(projectId, "T2");
        
        // 3. 创建子任务
        Long subtaskId = createSubTask(task1Id, "T1-1");
        
        // 验证子任务
        com.charles.server.reminder.entity.Task subtask = getTask(subtaskId);
        assertNotNull(subtask);
        assertEquals("T1-1", subtask.getTitle());
        assertEquals(task1Id, subtask.getParentTaskId());
    }
    
    @Test
    void scenario_parent_completion_cancellation_with_child() throws Exception {
        // 创建项目
        Long projectId = createProject("TestProject");
        
        // 创建父任务
        Long parentTaskId = createRootTask(projectId, "Parent");
        
        // 创建子任务
        Long childTaskId = createSubTask(parentTaskId, "Child");
        
        // 初始状态：都未完成
        com.charles.server.reminder.entity.Task parentTask = getTask(parentTaskId);
        com.charles.server.reminder.entity.Task childTask = getTask(childTaskId);
        assertFalse(parentTask.getIsCompleted());
        assertFalse(parentTask.getIsAbandoned());
        assertFalse(childTask.getIsCompleted());
        assertFalse(childTask.getIsAbandoned());
        
        // 完成父任务
        updateTaskCompletedStatus(parentTaskId, true);
        
        // 验证：父任务和子任务都完成
        parentTask = getTask(parentTaskId);
        childTask = getTask(childTaskId);
        assertTrue(parentTask.getIsCompleted());
        assertFalse(parentTask.getIsAbandoned());
        assertTrue(childTask.getIsCompleted());
        assertFalse(childTask.getIsAbandoned());
        
        // 取消父任务
        updateTaskCompletedStatus(parentTaskId, false);
        
        // 验证：父任务取消，子任务也取消
        parentTask = getTask(parentTaskId);
        childTask = getTask(childTaskId);
        assertFalse(parentTask.getIsCompleted());
        assertFalse(parentTask.getIsAbandoned());
        assertFalse(childTask.getIsCompleted());
        assertFalse(childTask.getIsAbandoned());
    }
    
    @Test
    void scenario_child_completion_affects_parent() throws Exception {
        // 创建项目
        Long projectId = createProject("TestProject2");
        
        // 创建父任务
        Long parentTaskId = createRootTask(projectId, "Parent2");
        
        // 创建子任务
        Long childTaskId = createSubTask(parentTaskId, "Child2");
        
        // 完成父任务
        updateTaskCompletedStatus(parentTaskId, true);
        
        // 验证：父任务和子任务都完成
        com.charles.server.reminder.entity.Task parentTask = getTask(parentTaskId);
        com.charles.server.reminder.entity.Task childTask = getTask(childTaskId);
        assertTrue(parentTask.getIsCompleted());
        assertTrue(childTask.getIsCompleted());
        
        // 取消子任务
        updateTaskCompletedStatus(childTaskId, false);
        
        // 验证：子任务取消，父任务也取消
        parentTask = getTask(parentTaskId);
        childTask = getTask(childTaskId);
        assertFalse(parentTask.getIsCompleted());
        assertFalse(childTask.getIsCompleted());
        
        // 重新完成子任务
        updateTaskCompletedStatus(childTaskId, true);
        
        // 验证：子任务完成，父任务也完成
        parentTask = getTask(parentTaskId);
        childTask = getTask(childTaskId);
        assertTrue(parentTask.getIsCompleted());
        assertTrue(childTask.getIsCompleted());
    }
    
    @Test
    void scenario_abandoned_status_propagation() throws Exception {
        // 创建项目
        Long projectId = createProject("TestProject3");
        
        // 创建父任务
        Long parentTaskId = createRootTask(projectId, "Parent3");
        
        // 创建子任务
        Long childTaskId = createSubTask(parentTaskId, "Child3");
        
        // 废弃父任务
        updateTaskAbandonedStatus(parentTaskId, true);
        
        // 验证：父任务和子任务都废弃
        com.charles.server.reminder.entity.Task parentTask = getTask(parentTaskId);
        com.charles.server.reminder.entity.Task childTask = getTask(childTaskId);
        assertTrue(parentTask.getIsAbandoned());
        assertTrue(childTask.getIsAbandoned());
        
        // 恢复父任务
        updateTaskAbandonedStatus(parentTaskId, false);
        
        // 验证：父任务恢复，子任务也恢复
        parentTask = getTask(parentTaskId);
        childTask = getTask(childTaskId);
        assertFalse(parentTask.getIsAbandoned());
        assertFalse(childTask.getIsAbandoned());
    }
}