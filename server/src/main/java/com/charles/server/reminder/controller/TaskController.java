package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.dto.TaskDeleteRequest;
import com.charles.server.reminder.dto.TaskGetAllRequest;
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

    /**************************************************************************************/
    /*                                    Basic CRUD                                      */
    /**************************************************************************************/

    // Create Task
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody @Valid TaskCreateRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            taskService.create(userId, dto);
            log.info("Task created successfully for user: {}", userId);
            return ResponseUtils.buildEmptySuccessResponse("Task created successfully");
        } catch (Exception e) {
            log.error("Task Create Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Delete Task
    @PostMapping("delete")
    public Map<String, Object> delete(@RequestBody @Valid TaskDeleteRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            taskService.deleteById(userId, dto.getTaskId());
            log.info("Task deleted successfully for user: {}, taskId: {}", userId, dto.getTaskId());
            return ResponseUtils.buildEmptySuccessResponse("Task deleted successfully");
        } catch (Exception e) {
            log.error("Task Delete Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Update Task
    @PostMapping("update")
    public Map<String, Object> updateById(@RequestBody @Valid TaskUpdateRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            taskService.update(userId, dto);
            return ResponseUtils.buildEmptySuccessResponse("Task updated successfully");
        } catch (Exception e) {
            log.error("Task Update Failed: {}", e.getMessage(), e);
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
            log.error("Task Batch Update Position Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Get All Tasks
    @GetMapping("get-all")
    public Map<String, Object> getAll(@RequestBody @Valid TaskGetAllRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Task> tasks = taskService.getAll(userId, dto);
            log.info("Get All Tasks Successfully for user: {}", userId);
            return ResponseUtils.buildSuccessResponse(tasks, "Get All Tasks Successfully");
        } catch (Exception e) {
            log.error("Get All Tasks Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    /**************************************************************************************/
    /*                                    xxxxx                                           */
    /**************************************************************************************/



    // 更新任务状态
    // @PutMapping("update-status/{id}")
    // public Map<String, Object> updateStatus(@PathVariable("id") Long taskId, 
    //                                      @RequestParam("status") String status, 
    //                                      HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         taskService.updateStatus(userId, taskId, status);
    //         log.info("Update Task Status Successfully for user: {}, taskId: {}, status: {}", userId, taskId, status);
    //         return ResponseUtils.buildEmptySuccessResponse("Update Task Status Successfully");
    //     } catch (Exception e) {
    //         log.error("Update Task Status Failed: {}", e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse(e.getMessage());
    //     }
    // }

    // 获取特定状态的任务
    // @GetMapping("get-by-status")
    // public Map<String, Object> getByStatus(@RequestParam("status") String status, 
    //                                      HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         List<Task> tasks = taskService.getByStatus(userId, status);
    //         return ResponseUtils.buildSuccessResponse(tasks, "任务查询成功");
    //     } catch (Exception e) {
    //         log.error("获取特定状态任务失败: {}", e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse(e.getMessage());
    //     }
    // }

    // 获取子任务
    // @GetMapping("get-sub-tasks/{parentTaskId}")
    // public Map<String, Object> getSubTasks(@PathVariable("parentTaskId") Long parentTaskId, 
    //                                     HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         List<Task> subTasks = taskService.getSubTasks(userId, parentTaskId);
    //         return ResponseUtils.buildSuccessResponse(subTasks, "子任务查询成功");
    //     } catch (Exception e) {
    //         log.error("获取子任务失败: {}", e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse(e.getMessage());
    //     }
    // }

    // 获取即将截止的任务
    // @GetMapping("get-upcoming")
    // public Map<String, Object> getUpcomingTasks(@RequestParam("days") Integer days, 
    //                                          HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         LocalDateTime dueDate = LocalDateTime.now().plusDays(days != null ? days : 7);
    //         List<Task> upcomingTasks = taskService.getUpcomingTasks(userId, dueDate);
    //         return ResponseUtils.buildSuccessResponse(upcomingTasks, "即将截止任务查询成功");
    //     } catch (Exception e) {
    //         log.error("获取即将截止任务失败: {}", e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse(e.getMessage());
    //     }
    // }
}
