package com.charles.server.reminder.service;

import java.time.LocalDateTime;
import java.util.List;

import com.charles.server.reminder.entity.History;

public interface HistoryService {
    // 创建新的历史记录
    History create(History history);
    
    // 根据ID获取历史记录
    History getById(Long historyId);
    
    // 根据任务ID和当前次数获取历史记录
    History getByTaskIdAndCurrent(Long taskId, Integer current);
    
    // 获取任务的所有历史记录
    List<History> getByTaskId(Long taskId);
    
    // 获取用户的所有历史记录
    List<History> getByUserId(Long userId);
    
    // 获取用户特定状态的历史记录
    List<History> getByUserIdAndStatus(Long userId, String status);
    
    // 更新历史记录
    History updateById(History history);
    
    // 更新历史记录状态
    int updateStatus(Long historyId, String status);
    
    // 获取用户在日期范围内的历史记录
    List<History> getByUserIdAndDateRange(Long userId, LocalDateTime startDate, LocalDateTime endDate);
    
    // 删除任务的所有历史记录
    int deleteByTaskId(Long taskId);
}