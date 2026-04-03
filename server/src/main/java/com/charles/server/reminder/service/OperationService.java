package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Operation;

public interface OperationService {
    
    /**
     * Get next operation ID
     * @param userId
     */
    Long getId(Long userId);
    
    /**
     * Record operation
     * @param operation
     * @return operation ID
     */
    Long create(Operation operation);
    
    /**
     * Revert latest operation
     * @param userId
     */
    void revert(Long userId);
}