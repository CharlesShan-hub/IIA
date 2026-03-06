package com.charles.server.reminder.service;

import java.time.LocalDateTime;
import java.util.List;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.entity.Task;

public interface TaskService {
    /**
     * Create Task
     */
    void create(Long userId, TaskCreateRequest dto);

    /** Update Task */
    void update(Long userId, TaskUpdateRequest dto);

    /**
     * Delete Task
     */
    void deleteById(Long userId, Long taskId);

    /**
     * Delete all tasks in a project
     */
    void deleteByProjectId(Long userId, Long projectId);

    /**
     * Batch update the sort order of tasks
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest dto);
    
    /**
     * Batch update the project_id of tasks (project_id may be null to indicate default area)
     */
    void batchUpdateProjectId(Long userId, ProjectDeleteRequest dto);
    
    // 获取用户所有任务
    List<Task> getAll(Long userId);
    
    // 根据ID获取任务
    Task getById(Long taskId);
    
    // 更新任务
    boolean updateById(Task task);
    
    // 更新任务状态
    void updateStatus(Long userId, Long taskId, String status);
    
    // 获取用户特定状态的任务
    List<Task> getByStatus(Long userId, String status);
    
    // 获取用户特定项目的任务
    List<Task> getByProjectId(Long userId, Long projectId);
    
    // 获取子任务
    List<Task> getSubTasks(Long userId, Long parentTaskId);
    
    // 获取即将截止的任务
    List<Task> getUpcomingTasks(Long userId, LocalDateTime dueDate);

}
