package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.History;
import com.charles.server.reminder.mapper.HistoryMapper;
import com.charles.server.reminder.service.HistoryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class HistoryServiceImpl implements HistoryService {
    
    private final HistoryMapper historyMapper;
    
    @Override
    public Long generateNextOperationId() {
        // 使用数据库序列或时间戳生成操作ID
        // 这里使用简单的自增方式
        Long maxOperationId = historyMapper.getMaxOperationId();
        return (maxOperationId == null) ? 1L : maxOperationId + 1;
    }

    // private Long getLastOperationId(Long taskId) {
    //     History lastHistory = historyMapper.findLatestByTaskId(taskId);
    //     if (lastHistory != null) {
    //         return lastHistory.getOperationId();
    //     }
    //     return null;
    // }
    
    @Override
    @Transactional
    public void create(History history) {
        // 设置创建时间
        history.setCreatedAt(LocalDateTime.now());
        
        // 插入历史记录
        historyMapper.insert(history);
        log.debug("创建状态变更历史: taskId={}, isCompleted={}, isAbandoned={}, isSkipped={}, operationId={}", 
                 history.getTaskId(), history.getIsCompleted(), history.getIsAbandoned(), 
                 history.getIsSkipped(), history.getOperationId());
    }
    
    @Override
    public List<History> findByOperationId(Long operationId) {
        return historyMapper.findByOperationId(operationId);
    }
    
    @Override
    public History findLatestByTaskId(Long taskId) {
        return historyMapper.findLatestByTaskId(taskId);
    }
    
    @Override
    public List<History> findByTaskId(Long taskId) {
        return historyMapper.findByTaskId(taskId);
    }
    
    @Override
    public History findLastCompletedHistory(Long taskId) {
        List<History> histories = historyMapper.findByTaskId(taskId);
        // 从最新到最旧查找第一个完成的历史记录
        for (int i = histories.size() - 1; i >= 0; i--) {
            History history = histories.get(i);
            if(Boolean.TRUE.equals(history.getIsCompleted())) {
                return history;
            }
        }
        return null;
    }
    
    @Override
    public boolean isOperationIdInTaskHistory(Long taskId, Long operationId) {
        List<History> histories = historyMapper.findByTaskId(taskId);
        for (History history : histories) {
            if(operationId.equals(history.getOperationId())) {
                return true;
            }
        }
        return false;
    }
    
    @Override
    @Transactional
    public void undoByOperationId(Long operationId) {
        // 1. 找到该操作批次的所有历史记录
        List<History> histories = historyMapper.findByOperationId(operationId);
        
        // 2. 生成撤销操作ID
        Long undoOperationId = generateNextOperationId();
        
        // 3. 为每个历史记录创建撤销记录
        for (History history : histories) {
            // 创建撤销记录（状态反向变更）
            create(History.builder()
                .taskId(history.getTaskId())
                .isCompleted(history.getIsCompleted())  // 当前完成状态
                .isAbandoned(history.getIsAbandoned())  // 当前废弃状态
                .isSkipped(history.getIsSkipped())      // 当前跳过状态
                .current(history.getCurrent())
                .operationId(undoOperationId)
                .build());
        }
        
        log.info("撤销操作批次: operationId={}, 生成撤销操作ID={}", operationId, undoOperationId);
    }
}