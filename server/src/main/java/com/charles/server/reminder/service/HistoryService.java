package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.History;
import java.util.List;

public interface HistoryService {
    
    /**
     * 生成新的操作ID
     */
    Long generateNextOperationId();
    
    /**
     * 创建状态变更历史记录
     * @param history 历史记录实体
     */
    void create(History history);
    
    /**
     * 根据操作ID查询历史记录
     */
    List<History> findByOperationId(Long operationId);
    
    /**
     * 查询任务的最新历史记录
     */
    History findLatestByTaskId(Long taskId);
    
    /**
     * 根据任务ID查询所有历史记录
     */
    List<History> findByTaskId(Long taskId);
    
    /**
     * 查找任务的上次完成历史记录
     */
    History findLastCompletedHistory(Long taskId);
    
    /**
     * 检查操作ID是否在任务的历史记录中
     */
    boolean isOperationIdInTaskHistory(Long taskId, Long operationId);
    
    /**
     * 根据操作ID批量撤销状态变更
     */
    void undoByOperationId(Long operationId);
}