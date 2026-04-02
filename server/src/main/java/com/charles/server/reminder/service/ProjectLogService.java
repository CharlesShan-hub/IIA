package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.ProjectLog;
import java.util.List;

public interface ProjectLogService {
    /**
     * Save project to history table
     * @param project project entity
     */
    void save(Project project);
    
    /**
     * Save project to history table with batch operation ID
     * @param project project entity
     * @param batchOperationId batch operation ID
     */
    void save(Project project, Long batchOperationId);
    
    /**
     * Find history records by project ID
     * @param projectId project ID
     * @return history record list
     */
    List<ProjectLog> findByProjectId(Long projectId);
    
    /**
     * Find history records by operation ID
     * @param operationId operation ID
     * @return history record list
     */
    List<ProjectLog> findByOperationId(Long operationId);
    
    /**
     * Find history records by batch operation ID
     * @param batchOperationId batch operation ID
     * @return history record list
     */
    List<ProjectLog> findByBatchOperationId(Long batchOperationId);
    
    /**
     * Revert an operation
     * @param userId the user ID
     * @param operationId the operation to be reverted
     * @param previousOperationId the previous operation ID
     */
    void revert(Long userId, Long operationId, Long previousOperationId);
}