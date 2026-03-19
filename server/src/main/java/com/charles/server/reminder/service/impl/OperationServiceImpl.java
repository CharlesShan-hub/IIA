package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.mapper.OperationMapper;
import com.charles.server.reminder.service.OperationService;
import com.charles.server.reminder.service.ProjectLogService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
@Slf4j
public class OperationServiceImpl implements OperationService {
    
    private final OperationMapper operationMapper;
    private final ProjectLogService projectLogService;
    
    @Override
    public Long getId(Long userId) {
        Long maxOperationId = operationMapper.getMaxOperationIdByUserId(userId);
        return (maxOperationId == null) ? 1L : maxOperationId + 1;
    }

    @Override
    public void revert(Long userId) {
        // 1. 获取用户最新的操作ID
        Long latestOperationId = operationMapper.getLatestOperationIdByUserId(userId);
        if (latestOperationId == null) {
            throw new IllegalStateException("用户没有可撤回的操作");
        }
        
        // 2. 获取操作详情（用于判断影响哪些表）
        Operation operation = operationMapper.findByIdAndUserId(latestOperationId, userId);
        
        // 3. 找到上一次的操作ID（对于新增操作，可能为null）
        Long previousOperationId = operationMapper.getPreviousOperationId(userId, latestOperationId);
        
        // 4. 根据受影响表恢复数据
        if (Boolean.TRUE.equals(operation.getIsReminderProject())) {
            projectLogService.revert(userId, latestOperationId, previousOperationId);
            log.debug("撤回项目操作完成: userId={}, operationId={}, previousOperationId={}", 
                    userId, latestOperationId, previousOperationId);
        }
        // TODO: 其他表的撤回逻辑
        
        // 5. 删除被撤回的操作记录
        int deletedOperations = operationMapper.deleteById(latestOperationId);
        
        log.info("撤回操作完成: userId={}, latestOperationId={}, previousOperationId={}, deletedOperations={}", 
                userId, latestOperationId, previousOperationId, deletedOperations);
    }
    
    @Override
    public void create(Operation operation) {
        operation.setPerformedAt(LocalDateTime.now());
        operationMapper.insert(operation);
        log.debug("记录操作: operationId={}, userId={}", operation.getOperationId(), operation.getUserId());
    }
}