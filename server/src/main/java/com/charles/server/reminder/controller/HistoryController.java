package com.charles.server.reminder.controller;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.entity.History;
import com.charles.server.reminder.service.HistoryService;
import com.charles.server.utils.ResponseUtils;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/reminder/histories")
@RequiredArgsConstructor
public class HistoryController {

    private final HistoryService historyService;
    private final TokenService tokenService;

    // 创建历史记录
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody History history, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} creating history record", userId);
            
            History createdHistory = historyService.create(history);
            return ResponseUtils.buildSuccessResponse(createdHistory, "历史记录创建成功");
        } catch (Exception e) {
            log.error("创建历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取所有历史记录
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching all history records", userId);
            
            List<History> historyList = historyService.getByUserId(userId);
            return ResponseUtils.buildSuccessResponse(historyList, "历史记录获取成功");
        } catch (Exception e) {
            log.error("获取历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 根据ID获取历史记录
    @GetMapping("get/{id}")
    public Map<String, Object> getById(@PathVariable("id") Long historyId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching history record by ID: {}", userId, historyId);
            
            History history = historyService.getById(historyId);
            if (history == null) {
                return ResponseUtils.buildErrorResponse("历史记录不存在");
            }
            return ResponseUtils.buildSuccessResponse(history, "历史记录获取成功");
        } catch (Exception e) {
            log.error("获取历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 更新历史记录
    @PutMapping("update/{id}")
    public Map<String, Object> updateById(@PathVariable("id") Long historyId, @RequestBody History history, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} updating history record: {}", userId, historyId);
            
            // 设置ID以确保更新正确的记录
            history.setHistoryId(historyId);
            History updatedHistory = historyService.updateById(history);
            return ResponseUtils.buildSuccessResponse(updatedHistory, "历史记录更新成功");
        } catch (Exception e) {
            log.error("更新历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 更新历史记录状态
    @PutMapping("update-status")
    public Map<String, Object> updateStatus(@RequestParam Long historyId, 
                                           @RequestParam String status, 
                                           HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} updating status of history record ID: {} to {}", userId, historyId, status);
            
            int result = historyService.updateStatus(historyId, status);
            if (result > 0) {
                return ResponseUtils.buildSuccessResponse("历史记录状态更新成功");
            } else {
                return ResponseUtils.buildErrorResponse("历史记录不存在或更新失败");
            }
        } catch (Exception e) {
            log.error("更新历史记录状态失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 根据状态获取历史记录
    @GetMapping("get-by-status/{status}")
    public Map<String, Object> getByStatus(@PathVariable String status, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching history records by status: {}", userId, status);
            
            List<History> historyList = historyService.getByUserIdAndStatus(userId, status);
            return ResponseUtils.buildSuccessResponse(historyList, "历史记录获取成功");
        } catch (Exception e) {
            log.error("获取历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取日期范围内的历史记录
    @GetMapping("get-by-date-range")
    public Map<String, Object> getByDateRange(@RequestParam String startDate, 
                                            @RequestParam String endDate, 
                                            HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching history records between {} and {}", userId, startDate, endDate);
            
            // 解析日期字符串为LocalDateTime
            LocalDateTime start = LocalDateTime.parse(startDate);
            LocalDateTime end = LocalDateTime.parse(endDate);
            
            List<History> historyList = historyService.getByUserIdAndDateRange(userId, start, end);
            return ResponseUtils.buildSuccessResponse(historyList, "历史记录获取成功");
        } catch (Exception e) {
            log.error("获取历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取任务的历史记录
    @GetMapping("get-by-task/{taskId}")
    public Map<String, Object> getByTaskId(@PathVariable Long taskId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching history records by task ID: {}", userId, taskId);
            
            List<History> historyList = historyService.getByTaskId(taskId);
            return ResponseUtils.buildSuccessResponse(historyList, "历史记录获取成功");
        } catch (Exception e) {
            log.error("获取历史记录失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}