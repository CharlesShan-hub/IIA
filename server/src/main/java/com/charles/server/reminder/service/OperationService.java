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

    /**
     * Create initial (zero) operation as the baseline anchor of a new user's operation chain
     * @param userId
     * @return operation ID
     */
    Long createZero(Long userId);
}