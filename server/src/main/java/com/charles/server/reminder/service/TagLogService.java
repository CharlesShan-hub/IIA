package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.TagLog;
import java.util.List;

public interface TagLogService {
    /**
     * Save tag to history table
     * @param tag tag entity
     */
    void save(Tag tag);
    
    /**
     * Save tag to history table (with batch operation ID)
     * @param tag tag entity
     * @param batchOperationId batch operation ID
     */
    void save(Tag tag, Long batchOperationId);
    
    /**
     * Find history records by tag ID
     * @param tagId tag ID
     * @return history record list
     */
    List<TagLog> findByTagId(Long tagId);
    
    /**
     * Find history records by operation ID
     * @param operationId operation ID
     * @return history record list
     */
    List<TagLog> findByOperationId(Long operationId);
    
    /**
     * Find history records by batch operation ID
     * @param batchOperationId batch operation ID
     * @return history record list
     */
    List<TagLog> findByBatchOperationId(Long batchOperationId);
    
    /**
     * Revert an operation
     * @param userId the user ID
     * @param operationId the operation to be reverted
     * @param previousOperationId the previous operation ID
     */
    void revert(Long userId, Long operationId, Long previousOperationId);
}