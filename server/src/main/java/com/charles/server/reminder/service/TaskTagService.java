package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.TaskTagCreateRequest;
import com.charles.server.reminder.dto.TaskTagDeleteRequest;
import com.charles.server.reminder.dto.TaskTagBatchCreateRequest;
import com.charles.server.reminder.dto.TaskTagBatchDeleteRequest;

public interface TaskTagService {
    /**
     * Create a new task-tag association
     * @param userId
     * @param dto the request body containing task ID and tag ID
     */
    void create(Long userId, TaskTagCreateRequest dto);

    /**
     * Create multiple task-tag associations in batch
     * @param userId
     * @param dto the request body containing task ID and tag ID list
     */
    void createBatch(Long userId, TaskTagBatchCreateRequest dto);

    /**
     * Delete a task-tag association
     * @param userId
     * @param dto the request body containing task ID and tag ID
     */
    void delete(Long userId, TaskTagDeleteRequest dto);
    
    /**
     * Delete multiple task-tag associations in batch
     * @param userId
     * @param dto the request body containing task ID and tag ID list
     */
    void deleteBatch(Long userId, TaskTagBatchDeleteRequest dto);
}
