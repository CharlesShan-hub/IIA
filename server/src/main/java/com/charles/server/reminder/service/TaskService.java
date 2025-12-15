package com.charles.server.reminder.service;

import java.time.LocalDateTime;
import java.util.List;

import com.charles.server.reminder.dto.CreateTaskRequest;
import com.charles.server.reminder.entity.Task;

public interface TaskService {
    /**
     * Create Task
     * @param userId user id
     * @param dto
     */
    void create(Long userId, CreateTaskRequest dto);
    
    // 获取用户所有任务
    List<Task> getAll(Long userId);
    
    // 根据ID获取任务
    Task getById(Long taskId);
    
    // 更新任务
    boolean updateById(Task task);
    
    // 更新任务状态
    boolean updateStatus(Long taskId, String status);
    
    // 获取用户特定状态的任务
    List<Task> getByStatus(Long userId, String status);
    
    // 获取用户特定项目的任务
    List<Task> getByProjectId(Long userId, Long projectId);
    
    // 获取子任务
    List<Task> getSubTasks(Long userId, Long parentTaskId);
    
    // 获取即将截止的任务
    List<Task> getUpcomingTasks(Long userId, LocalDateTime dueDate);
}