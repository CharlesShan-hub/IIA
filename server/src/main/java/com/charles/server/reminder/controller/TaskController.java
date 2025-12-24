package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;
import java.time.LocalDateTime;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.CreateTaskRequest;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

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
    public Map<String, Object> create(@RequestBody @Valid CreateTaskRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            taskService.create(userId, dto);
            log.info("Task created successfully for user: {}", userId);
            return ResponseUtils.buildEmptySuccessResponse("Task created successfully");
        } catch (Exception e) {
            log.error("Create task failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Delete Task
    @PostMapping("delete")
    public Map<String, Object> deleteById(@RequestParam Long taskId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            taskService.deleteById(userId, taskId);
            log.info("Task deleted successfully for user: {}", userId);
            return ResponseUtils.buildEmptySuccessResponse("Task deleted successfully");
        } catch (Exception e) {
            log.error("Delete task failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Batch Update Task Positions
    @PostMapping("batch-update-position")
    public Map<String, Object> batchUpdatePosition(@RequestBody @Valid BatchUpdatePositionRequest dto, HttpServletRequest httpRequest) {
        try {
            Long userId = tokenService.getUserIdFromRequest(httpRequest);
            taskService.batchUpdatePosition(userId, dto);
            log.info("User {} batch update task positions successfully, updated tasks: {}",
                 userId, dto.getPos());
            return ResponseUtils.buildEmptySuccessResponse("Reminder Tasks Positions Updated");
        } catch (Exception e) {
            log.error("Reminder Task Batch Update Task Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Get All Tasks
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Task> tasks = taskService.getAll(userId);
            log.info("Get All Tasks Successfully for user: {}", userId);
            return ResponseUtils.buildSuccessResponse(tasks, "Get All Tasks Successfully");
        } catch (Exception e) {
            log.error("Get All Tasks Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 更新任务
    @PutMapping("update/{id}")
    public Map<String, Object> updateById(@PathVariable("id") Long taskId, @RequestBody Task task, 
                                        HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            task.setTaskId(taskId);
            task.setUserId(userId);
            boolean updated = taskService.updateById(task);
            if (updated) {
                return ResponseUtils.buildEmptySuccessResponse("任务更新成功");
            } else {
                return ResponseUtils.buildErrorResponse("任务更新失败或无权限");
            }
        } catch (Exception e) {
            log.error("更新任务失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 更新任务状态
    @PutMapping("update-status/{id}")
    public Map<String, Object> updateStatus(@PathVariable("id") Long taskId, 
                                         @RequestParam("status") String status, 
                                         HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            taskService.updateStatus(userId, taskId, status);
            log.info("Update Task Status Successfully for user: {}, taskId: {}, status: {}", userId, taskId, status);
            return ResponseUtils.buildEmptySuccessResponse("Update Task Status Successfully");
        } catch (Exception e) {
            log.error("Update Task Status Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取特定状态的任务
    @GetMapping("get-by-status")
    public Map<String, Object> getByStatus(@RequestParam("status") String status, 
                                         HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Task> tasks = taskService.getByStatus(userId, status);
            return ResponseUtils.buildSuccessResponse(tasks, "任务查询成功");
        } catch (Exception e) {
            log.error("获取特定状态任务失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取特定项目的任务
    @GetMapping("get-by-project/{projectId}")
    public Map<String, Object> getByProjectId(@PathVariable("projectId") Long projectId, 
                                           HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Task> tasks = taskService.getByProjectId(userId, projectId);
            return ResponseUtils.buildSuccessResponse(tasks, "任务查询成功");
        } catch (Exception e) {
            log.error("获取特定项目任务失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取子任务
    @GetMapping("get-sub-tasks/{parentTaskId}")
    public Map<String, Object> getSubTasks(@PathVariable("parentTaskId") Long parentTaskId, 
                                        HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Task> subTasks = taskService.getSubTasks(userId, parentTaskId);
            return ResponseUtils.buildSuccessResponse(subTasks, "子任务查询成功");
        } catch (Exception e) {
            log.error("获取子任务失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取即将截止的任务
    @GetMapping("get-upcoming")
    public Map<String, Object> getUpcomingTasks(@RequestParam("days") Integer days, 
                                             HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            LocalDateTime dueDate = LocalDateTime.now().plusDays(days != null ? days : 7);
            List<Task> upcomingTasks = taskService.getUpcomingTasks(userId, dueDate);
            return ResponseUtils.buildSuccessResponse(upcomingTasks, "即将截止任务查询成功");
        } catch (Exception e) {
            log.error("获取即将截止任务失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}