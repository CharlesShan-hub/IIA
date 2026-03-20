package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.TaskTagCreateDTO;
import com.charles.server.reminder.dto.TaskTagDeleteDTO;
import com.charles.server.reminder.dto.TaskTagBatchCreateDTO;
import com.charles.server.reminder.dto.TaskTagBatchDeleteDTO;

public interface TaskTagService {
    /**
     * Create a new task-tag association
     * @param userId
     * @param dto the request body containing task ID and tag ID
     */
    void create(Long userId, TaskTagCreateDTO dto);

    /**
     * Create multiple task-tag associations in batch
     * @param userId
     * @param dto the request body containing task ID and tag ID list
     */
    void createBatch(Long userId, TaskTagBatchCreateDTO dto);

    /**
     * Delete a task-tag association
     * @param userId
     * @param dto the request body containing task ID and tag ID
     */
    void delete(Long userId, TaskTagDeleteDTO dto);
    
    /**
     * Delete multiple task-tag associations in batch
     * @param userId
     * @param dto the request body containing task ID and tag ID list
     */
    void deleteBatch(Long userId, TaskTagBatchDeleteDTO dto);
}
