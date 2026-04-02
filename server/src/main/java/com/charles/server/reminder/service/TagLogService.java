package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.TagLog;
import java.util.List;

public interface TagLogService {
    /**
     * 保存标签到历史表
     * @param tag 标签实体
     */
    void save(Tag tag);
    
    /**
     * 保存标签到历史表（带批量操作ID）
     * @param tag 标签实体
     * @param batchOperationId 批量操作ID
     */
    void save(Tag tag, Long batchOperationId);
    
    /**
     * 根据标签ID查找历史记录
     * @param tagId 标签ID
     * @return 历史记录列表
     */
    List<TagLog> findByTagId(Long tagId);
    
    /**
     * 根据操作ID查找历史记录
     * @param operationId 操作ID
     * @return 历史记录列表
     */
    List<TagLog> findByOperationId(Long operationId);
    
    /**
     * 根据批量操作ID查找历史记录
     * @param batchOperationId 批量操作ID
     * @return 历史记录列表
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