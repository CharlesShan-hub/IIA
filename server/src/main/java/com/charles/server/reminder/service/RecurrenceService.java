package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Recurrence;
import java.time.LocalDateTime;
import java.util.List;

public interface RecurrenceService {
    
    /**
     * 创建循环任务配置
     */
    int create(Recurrence recurrence);
    
    /**
     * 根据任务ID查询循环配置
     */
    Recurrence getByTaskId(Long taskId);
    
    /**
     * 更新循环任务配置
     */
    int update(Recurrence recurrence);
    
    /**
     * 更新下一次发生时间
     */
    int updateNextTime(Long taskId, LocalDateTime nextTime);
    
    /**
     * 更新重复次数
     */
    int updateCount(Long taskId, Integer count);
    
    /**
     * 删除循环任务配置
     */
    int deleteByTaskId(Long taskId);
    
    /**
     * 查询用户即将发生的循环任务
     */
    List<Recurrence> getUpcomingByUserId(Long userId, LocalDateTime deadline);
}