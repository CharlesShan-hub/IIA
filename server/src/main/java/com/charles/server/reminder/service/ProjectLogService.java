package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.ProjectLog;
import java.util.List;

public interface ProjectLogService {
    /**
     * 保存项目到历史表
     * @param project 项目实体
     */
    void save(Project project);
    
    /**
     * 保存项目到历史表（带批量操作ID）
     * @param project 项目实体
     * @param batchOperationId 批量操作ID
     */
    void save(Project project, Long batchOperationId);
    
    /**
     * 根据项目ID查找历史记录
     * @param projectId 项目ID
     * @return 历史记录列表
     */
    List<ProjectLog> findByProjectId(Long projectId);
    
    /**
     * 根据操作ID查找历史记录
     * @param operationId 操作ID
     * @return 历史记录列表
     */
    List<ProjectLog> findByOperationId(Long operationId);
    
    /**
     * 根据批量操作ID查找历史记录
     * @param batchOperationId 批量操作ID
     * @return 历史记录列表
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