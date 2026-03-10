package com.charles.server.reminder.controller;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.TaskTagCreateRequest;
import com.charles.server.reminder.dto.TaskTagDeleteRequest;
import com.charles.server.reminder.dto.TaskTagBatchCreateRequest;
import com.charles.server.reminder.dto.TaskTagBatchDeleteRequest;
import com.charles.server.reminder.service.TaskTagService;
import com.charles.server.utils.ResponseUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/reminder/task-tags")
@RequiredArgsConstructor
public class TaskTagController {

    private final TaskTagService taskTagService;
    private final TokenService tokenService;

    // Create a new task-tag association
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody TaskTagCreateRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} creating task-tag association: taskId={}, tagId={}, cascade={}", userId, dto.getTaskId(), dto.getTagId(), dto.getIncludeSubtasks());
            taskTagService.create(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "Task-tag association created successfully");
        } catch (Exception e) {
            log.error("Failed to create task-tag association: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Delete a task-tag association
    @PostMapping("delete")
    public Map<String, Object> delete(@RequestBody TaskTagDeleteRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} deleting task-tag association: taskId={}, tagId={}, cascade={}", userId, dto.getTaskId(), dto.getTagId(), dto.getIncludeSubtasks());
            taskTagService.delete(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "Task-tag association deleted successfully");
        } catch (Exception e) {
            log.error("Failed to delete task-tag association: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Create multiple task-tag associations in batch
    @PostMapping("batch-create")
    public Map<String, Object> batchCreate(@RequestBody TaskTagBatchCreateRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} batch creating task-tag associations: taskId={}, tagIds={}, cascade={}", userId, dto.getTaskId(), dto.getTagIds(), dto.getIncludeSubtasks());
            taskTagService.createBatch(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "Batch task-tag associations created successfully");
        } catch (Exception e) {
            log.error("Failed to batch create task-tag associations: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Delete multiple task-tag associations in batch
    @PostMapping("batch-delete")
    public Map<String, Object> batchDelete(@RequestBody TaskTagBatchDeleteRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} batch deleting task-tag associations: taskId={}, tagIds={}, cascade={}", userId, dto.getTaskId(), dto.getTagIds(), dto.getIncludeSubtasks());
            taskTagService.deleteBatch(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "Batch task-tag associations deleted successfully");
        } catch (Exception e) {
            log.error("Failed to batch delete task-tag associations: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}
