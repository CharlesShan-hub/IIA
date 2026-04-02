package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.mapper.OperationMapper;
import com.charles.server.reminder.service.OperationService;
import com.charles.server.reminder.service.ProjectLogService;
import com.charles.server.reminder.service.TagLogService;
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
    private final TagLogService tagLogService;
    
    @Override
    public Long getId(Long userId) {
        Long maxOperationId = operationMapper.getMaxOperationIdByUserId(userId);
        return (maxOperationId == null) ? 1L : maxOperationId + 1;
    }

    @Override
    public void revert(Long userId) {
        // 1. Get the latest operation ID of the user
        Long latestOperationId = operationMapper.getLatestOperationIdByUserId(userId);
        if (latestOperationId == null) {
            throw new IllegalStateException("No revertible operation for the user");
        }

        // 2. Find the previous operation ID
        Long previousOperationId = operationMapper.getPreviousOperationId(userId, latestOperationId);
        if (previousOperationId == null) {
            // If no previous operation ID exists, it means we are at the earliest "base" state (zero operation), revert is not allowed
            log.info("User {} attempted to revert the initial state, operation ignored", userId);
            throw new IllegalStateException("No more operations to revert");
        }

        // 3. Fetch operation details (to determine which tables are affected)
        Operation operation = operationMapper.findByIdAndUserId(latestOperationId, userId);

        // 4. Restore data based on affected tables
        if (Boolean.TRUE.equals(operation.getIsReminderProject())) {
            projectLogService.revert(userId, latestOperationId, previousOperationId);
            log.debug("Project operation reverted: userId={}, operationId={}, previousOperationId={}",
                    userId, latestOperationId, previousOperationId);
        }
        
        if (Boolean.TRUE.equals(operation.getIsReminderTag())) {
            tagLogService.revert(userId, latestOperationId, previousOperationId);
            log.debug("Tag operation reverted: userId={}, operationId={}, previousOperationId={}",
                    userId, latestOperationId, previousOperationId);
        }
        // TODO: Revert logic for other tables

        // 5. Delete the reverted operation record
        int deletedOperations = operationMapper.deleteById(latestOperationId);

        log.info("Revert operation completed: userId={}, latestOperationId={}, previousOperationId={}, deletedOperations={}",
                userId, latestOperationId, previousOperationId, deletedOperations);
    }
    
    @Override
    public void create(Operation operation) {
        operation.setPerformedAt(LocalDateTime.now());
        operationMapper.insert(operation);
        log.debug("Create operation success: operationId={}, userId={}", operation.getOperationId(), operation.getUserId());
    }
}