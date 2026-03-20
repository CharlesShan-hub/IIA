package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.TaskCreateDTO;
import com.charles.server.reminder.dto.TaskUpdateDTO;

public interface RecurrenceService {
    
    /**
     * Create a new recurrence config from TaskCreateRequest and taskId
     */
    void create(Long taskId, TaskCreateDTO dto);

    /**
     * Create or update recurrence config from TaskUpdateRequest and taskId
     */
    void update(Long taskId, TaskUpdateDTO dto);

    /**
     * Complete a recurring task
     */
    void complete(Long taskId);

    /**
     * Delete recurrence and history occurrences
    */
    void delete(Long taskId);
}