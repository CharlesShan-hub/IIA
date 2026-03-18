package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Operation;

public interface OperationService {
    
    /**
     * 获取下一个操作ID
     * @param userId 用户ID
     */
    Long getId(Long userId);
    
    /**
     * 记录操作
     * @param operation 操作实体
     */
    void create(Operation operation);
}