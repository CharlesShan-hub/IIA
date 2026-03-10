package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.dto.TaskDeleteRequest;
import com.charles.server.reminder.dto.TaskGetAllRequest;
import com.charles.server.reminder.dto.TaskStatusUpdateRequest;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.service.TaskService;
import com.charles.server.utils.ResponseUtils;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/reminder/task")
@RequiredArgsConstructor
public class TaskController {

    private final TaskService taskService;
    private final TokenService tokenService;

    // Create Task
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody @Valid TaskCreateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.create(userId, dto);
        log.info("Task created successfully for user: {}", userId);
        return ResponseUtils.buildEmptySuccessResponse("Task created successfully");
    }

    // Delete Task
    @PostMapping("delete")
    public Map<String, Object> delete(@RequestBody @Valid TaskDeleteRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.delete(userId, dto.getTaskId());
        log.info("Task deleted successfully for user: {}, taskId: {}", userId, dto.getTaskId());
        return ResponseUtils.buildEmptySuccessResponse("Task deleted successfully");
    }

    // Update Task
    @PostMapping("update")
    public Map<String, Object> update(@RequestBody @Valid TaskUpdateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.update(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Task updated successfully");
    }

    // Batch Update Task Positions
    @PostMapping("batch-update-position")
    public Map<String, Object> batchUpdatePosition(@RequestBody @Valid BatchUpdatePositionRequest dto, HttpServletRequest httpRequest) {
        Long userId = tokenService.getUserIdFromRequest(httpRequest);
        taskService.batchUpdatePosition(userId, dto);
        log.info("User {} batch update task positions successfully, updated tasks: {}",
             userId, dto.getPos());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Tasks Positions Updated");
    }

    // Get All Tasks
    @GetMapping("get-all")
    public Map<String, Object> getAll(@RequestBody @Valid TaskGetAllRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        List<Task> tasks = taskService.getAll(userId, dto);
        log.info("Get All Tasks Successfully for user: {}", userId);
        return ResponseUtils.buildSuccessResponse(tasks, "Get All Tasks Successfully");
    }

    // Update Task Status (taskId & status [done|todo|abandoned])
    @PatchMapping("update-status")
    public Map<String, Object> updateStatus(@RequestBody @Valid TaskStatusUpdateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.updateStatus(userId, dto);
        log.info("Update Task Status Successfully for user: {}, taskId: {}, status: {}", userId, dto.getTaskId(), dto.getStatus());
        return ResponseUtils.buildEmptySuccessResponse("Update Task Status Successfully");
    }
}
