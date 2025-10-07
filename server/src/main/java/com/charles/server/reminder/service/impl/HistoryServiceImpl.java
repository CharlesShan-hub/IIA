package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.History;
import com.charles.server.reminder.mapper.HistoryMapper;
import com.charles.server.reminder.service.HistoryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class HistoryServiceImpl implements HistoryService {

    private final HistoryMapper historyMapper;

    @Override
    public History create(History history) {
        log.info("Creating history record: {}", history);
        historyMapper.insert(history);
        log.info("Created history record with ID: {}", history.getHistoryId());
        return history;
    }

    @Override
    public History getById(Long historyId) {
        log.info("Getting history record by ID: {}", historyId);
        return historyMapper.findById(historyId);
    }

    @Override
    public History getByTaskIdAndCurrent(Long taskId, Integer current) {
        log.info("Getting history record by task ID: {} and current: {}", taskId, current);
        return historyMapper.findByTaskIdAndCurrent(taskId, current);
    }

    @Override
    public List<History> getByTaskId(Long taskId) {
        log.info("Getting all history records by task ID: {}", taskId);
        return historyMapper.findByTaskId(taskId);
    }

    @Override
    public List<History> getByUserId(Long userId) {
        log.info("Getting all history records by user ID: {}", userId);
        return historyMapper.findByUserId(userId);
    }

    @Override
    public List<History> getByUserIdAndStatus(Long userId, String status) {
        log.info("Getting history records by user ID: {} and status: {}", userId, status);
        return historyMapper.findByUserIdAndStatus(userId, status);
    }

    @Override
    public History updateById(History history) {
        log.info("Updating history record: {}", history);
        historyMapper.update(history);
        log.info("Updated history record with ID: {}", history.getHistoryId());
        return historyMapper.findById(history.getHistoryId());
    }

    @Override
    public int updateStatus(Long historyId, String status) {
        log.info("Updating status of history record ID: {} to {}", historyId, status);
        return historyMapper.updateStatus(historyId, status);
    }

    @Override
    public List<History> getByUserIdAndDateRange(Long userId, LocalDateTime startDate, LocalDateTime endDate) {
        log.info("Getting history records by user ID: {} between {} and {}", userId, startDate, endDate);
        return historyMapper.findByUserIdAndDateRange(userId, startDate, endDate);
    }

    @Override
    public int deleteByTaskId(Long taskId) {
        log.info("Deleting all history records by task ID: {}", taskId);
        return historyMapper.deleteByTaskId(taskId);
    }
}