package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;

public interface RecurrenceService {
    
    /**
     * Create a new recurrence config from TaskCreateRequest and taskId
     */
    void create(Long taskId, TaskCreateRequest dto);

    /**
     * Create or update recurrence config from TaskUpdateRequest and taskId
     */
    void update(Long taskId, TaskUpdateRequest dto);

    /**
     * Complete a recurring task
     */
    void complete(Long taskId);

    /**
     * Delete recurrence and history occurrences
    */
    void delete(Long taskId);
}