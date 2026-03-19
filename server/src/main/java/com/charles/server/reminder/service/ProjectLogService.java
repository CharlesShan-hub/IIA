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
     * Revert an operation
     * @param userId the user ID
     * @param operationId the operation to be reverted
     * @param previousOperationId the previous operation ID
     */
    void revert(Long userId, Long operationId, Long previousOperationId);
}