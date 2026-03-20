package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.dto.TaskCreateDTO;
import com.charles.server.reminder.dto.TaskUpdateDTO;
import com.charles.server.reminder.dto.ProjectDeleteDTO;
import com.charles.server.reminder.dto.TaskGetAllDTO;
import com.charles.server.reminder.dto.TaskUpdateCompletedDTO;
import com.charles.server.reminder.dto.TaskUpdateAbandonedDTO;

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
    void create(Long userId, TaskCreateDTO dto);

    /** Update Task
     * @param userId
     * @param dto the task update request
     */
    void update(Long userId, TaskUpdateDTO dto);

    /**
     * Delete Task and its sub-tasks
     * @param userId
     * @param taskId the task ID to delete
     */
    void delete(Long userId, Long taskId);
    
    /**
     * Batch update the sort order of tasks
     * @param userId
     * @param dto the batch update position request
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionDTO dto);
    
    /**
     * Get all tasks for a user (including tasks in default area)
     * @param userId
     * @param dto the task query request
     * @return the list of tasks matching the filter
     */
    List<Task> getAll(Long userId, TaskGetAllDTO dto);

    /**************************************************************************************/
    /*                                   Task Status                                      */
    /**************************************************************************************/

    /**
     * Update Task Completed Status
     * @param userId
     * @param dto the task update completed request
     */
    void updateCompletedStatus(Long userId, TaskUpdateCompletedDTO dto);
    
    /**
     * Update Task Abandoned Status
     * @param userId
     * @param dto the task update abandoned request
     */
    void updateAbandonedStatus(Long userId, TaskUpdateAbandonedDTO dto);

    /**************************************************************************************/
    /*                                   Recurrence Task                                  */
    /**************************************************************************************/


    /**************************************************************************************/
    /*                              Support Project Operation                             */
    /**************************************************************************************/

    /**
     * Batch update the project_id of tasks (project_id may be null to indicate default area)
     * @param userId
     * @param dto the project deletion request
     */
    void batchUpdateProjectId(Long userId, ProjectDeleteDTO dto);

    /**
     * Delete all tasks in a project
     * @param userId
     * @param projectId the project ID to delete
     */
    void deleteByProjectId(Long userId, Long projectId);
}
