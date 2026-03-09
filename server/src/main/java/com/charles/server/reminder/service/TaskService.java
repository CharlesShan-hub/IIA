package com.charles.server.reminder.service;

import java.time.LocalDateTime;
import java.util.List;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.TaskGetAllRequest;
import com.charles.server.reminder.dto.TaskStatusUpdateRequest;
import com.charles.server.reminder.entity.Task;

public interface TaskService {

    /**************************************************************************************/
    /*                                    Basic CRUD                                      */
    /**************************************************************************************/

    /**
     * Create Task
     * @param userId
     * @param dto the task creation request
     */
    void create(Long userId, TaskCreateRequest dto);

    /** Update Task
     * @param userId
     * @param dto the task update request
     */
    void update(Long userId, TaskUpdateRequest dto);

    /**
     * Delete Task and its sub-tasks
     * @param userId
     * @param taskId the task ID to delete
     */
    void delete(Long userId, Long taskId);

    /**
     * Delete all tasks in a project
     * @param userId
     * @param projectId the project ID to delete
     */
    void deleteByProjectId(Long userId, Long projectId);
    
    /**
     * Batch update the sort order of tasks
     * @param userId
     * @param dto the batch update position request
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest dto);
    
    /**
     * Get all tasks for a user (including tasks in default area)
     * @param userId
     * @param dto the task query request
     * @return the list of tasks matching the filter
     */
    List<Task> getAll(Long userId, TaskGetAllRequest dto);

    /**************************************************************************************/
    /*                              Support Project Operation                             */
    /**************************************************************************************/

    /**
     * Batch update the project_id of tasks (project_id may be null to indicate default area)
     * @param userId
     * @param dto the project deletion request
     */
    void batchUpdateProjectId(Long userId, ProjectDeleteRequest dto);

    /**************************************************************************************/
    /*                                   Task Status                                      */
    /**************************************************************************************/

    /**
     * Update Task Status (taskId & status [done|todo|abandoned])
     * @param userId
     * @param dto the task status update request
     */
    void updateStatus(Long userId, TaskStatusUpdateRequest dto);

    /**************************************************************************************/
    /*                                    Basic CRUD                                      */
    /**************************************************************************************/
    //下面是没改的






    /**
     * Get task by ID
     */
    // Task getById(Long taskId);
    
    // // 更新任务
    // boolean updateById(Task task);

    // // 获取用户特定状态的任务
    // List<Task> getByStatus(Long userId, String status);
    
    // // 获取用户特定项目的任务
    // List<Task> getByProjectId(Long userId, Long projectId);
    
    // // 获取子任务
    // List<Task> getSubTasks(Long userId, Long parentTaskId);
    
    // // 获取即将截止的任务
    // List<Task> getUpcomingTasks(Long userId, LocalDateTime dueDate);

}
