package com.charles.server.reminder.controller;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.TaskTagCreateDTO;
import com.charles.server.reminder.dto.TaskTagDeleteDTO;
import com.charles.server.reminder.dto.TaskTagBatchCreateDTO;
import com.charles.server.reminder.dto.TaskTagBatchDeleteDTO;
import com.charles.server.reminder.service.TaskTagService;
import com.charles.server.utils.ResponseUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;

@Slf4j
@RestController
@RequestMapping("/api/reminder/task-tags")
@RequiredArgsConstructor
public class TaskTagController {

    private final TaskTagService taskTagService;
    private final TokenService tokenService;

    // Create a new task-tag association
    @PostMapping("create")
    public ResponseUtils<Void> create(@RequestBody TaskTagCreateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("User {} creating task-tag association: taskId={}, tagId={}, cascade={}", userId, dto.getTaskId(), dto.getTagId(), dto.getIncludeSubtasks());
        taskTagService.create(userId, dto);
        return ResponseUtils.buildSuccessResponse(null, "Task-tag association created successfully");
    }

    // Delete a task-tag association
    @PostMapping("delete")
    public ResponseUtils<Void> delete(@RequestBody TaskTagDeleteDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("User {} deleting task-tag association: taskId={}, tagId={}, cascade={}", userId, dto.getTaskId(), dto.getTagId(), dto.getIncludeSubtasks());
        taskTagService.delete(userId, dto);
        return ResponseUtils.buildSuccessResponse(null, "Task-tag association deleted successfully");
    }

    // Create multiple task-tag associations in batch
    @PostMapping("batch-create")
    public ResponseUtils<Void> batchCreate(@RequestBody TaskTagBatchCreateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("User {} batch creating task-tag associations: taskId={}, tagIds={}, cascade={}", userId, dto.getTaskId(), dto.getTagIds(), dto.getIncludeSubtasks());
        taskTagService.createBatch(userId, dto);
        return ResponseUtils.buildSuccessResponse(null, "Batch task-tag associations created successfully");
    }

    // Delete multiple task-tag associations in batch
    @PostMapping("batch-delete")
    public ResponseUtils<Void> batchDelete(@RequestBody TaskTagBatchDeleteDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("User {} batch deleting task-tag associations: taskId={}, tagIds={}, cascade={}", userId, dto.getTaskId(), dto.getTagIds(), dto.getIncludeSubtasks());
        taskTagService.deleteBatch(userId, dto);
        return ResponseUtils.buildSuccessResponse(null, "Batch task-tag associations deleted successfully");
    }
}
