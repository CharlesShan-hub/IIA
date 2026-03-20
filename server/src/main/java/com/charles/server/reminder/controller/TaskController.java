package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.dto.TaskCreateDTO;
import com.charles.server.reminder.dto.TaskUpdateDTO;
import com.charles.server.reminder.dto.TaskDeleteDTO;
import com.charles.server.reminder.dto.TaskGetAllDTO;
import com.charles.server.reminder.dto.TaskUpdateCompletedDTO;
import com.charles.server.reminder.dto.TaskUpdateAbandonedDTO;
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
    public Map<String, Object> create(@RequestBody @Valid TaskCreateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.create(userId, dto);
        log.info("Task created successfully for user: {}", userId);
        return ResponseUtils.buildEmptySuccessResponse("Task created successfully");
    }

    // Delete Task
    @PostMapping("delete")
    public Map<String, Object> delete(@RequestBody @Valid TaskDeleteDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.delete(userId, dto.getTaskId());
        log.info("Task deleted successfully for user: {}, taskId: {}", userId, dto.getTaskId());
        return ResponseUtils.buildEmptySuccessResponse("Task deleted successfully");
    }

    // Update Task
    @PostMapping("update")
    public Map<String, Object> update(@RequestBody @Valid TaskUpdateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.update(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Task updated successfully");
    }

    // Batch Update Task Positions
    @PostMapping("batch-update-position")
    public Map<String, Object> batchUpdatePosition(@RequestBody @Valid BatchUpdatePositionDTO dto, HttpServletRequest httpRequest) {
        Long userId = tokenService.getUserIdFromRequest(httpRequest);
        taskService.batchUpdatePosition(userId, dto);
        log.info("User {} batch update task positions successfully, updated tasks: {}",
             userId, dto.getPos());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Tasks Positions Updated");
    }

    // Get All Tasks
    @GetMapping("get-all")
    public Map<String, Object> getAll(@RequestBody @Valid TaskGetAllDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        List<Task> tasks = taskService.getAll(userId, dto);
        log.info("Get All Tasks Successfully for user: {}", userId);
        return ResponseUtils.buildSuccessResponse(tasks, "Get All Tasks Successfully");
    }
    
    // Update Task Completed Status
    @PatchMapping("update-completed")
    public Map<String, Object> updateCompletedStatus(@RequestBody @Valid TaskUpdateCompletedDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.updateCompletedStatus(userId, dto);
        log.info("Update Task Completed Status Successfully for user: {}, taskId: {}, isCompleted: {}", 
                userId, dto.getTaskId(), dto.getIsCompleted());
        return ResponseUtils.buildEmptySuccessResponse("Update Task Completed Status Successfully");
    }
    
    // Update Task Abandoned Status
    @PatchMapping("update-abandoned")
    public Map<String, Object> updateAbandonedStatus(@RequestBody @Valid TaskUpdateAbandonedDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        taskService.updateAbandonedStatus(userId, dto);
        log.info("Update Task Abandoned Status Successfully for user: {}, taskId: {}, isAbandoned: {}", 
                userId, dto.getTaskId(), dto.getIsAbandoned());
        return ResponseUtils.buildEmptySuccessResponse("Update Task Abandoned Status Successfully");
    }
}
