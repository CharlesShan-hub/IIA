package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.mapper.OperationMapper;
import com.charles.server.reminder.service.OperationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
@Slf4j
public class OperationServiceImpl implements OperationService {
    
    private final OperationMapper operationMapper;
    
    @Override
    public Long getId(Long userId) {
        Long maxOperationId = operationMapper.getMaxOperationIdByUserId(userId);
        return (maxOperationId == null) ? 1L : maxOperationId + 1;
    }
    
    @Override
    public void create(Operation operation) {
        operation.setPerformedAt(LocalDateTime.now());
        operationMapper.insert(operation);
        log.debug("记录操作: operationId={}, userId={}", operation.getOperationId(), operation.getUserId());
    }
}