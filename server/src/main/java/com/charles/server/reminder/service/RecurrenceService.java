package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;

public interface RecurrenceService {
    
    /**
     * Create a new recurrence config from TaskCreateRequest and taskId
     */
    void create(Long taskId, TaskCreateRequest dto);

    /**
     * Create or update recurrence config from TaskUpdateRequest and taskId
     */
    void create(Long taskId, TaskUpdateRequest dto);

    /**
     * Delete recurrence and history occurrences
    */
    void deleteByTaskId(Long taskId);
    
    // /**
    //  * 根据任务ID查询循环配置
    //  */
    // Recurrence getByTaskId(Long taskId);
    
    // /**
    //  * 更新循环任务配置
    //  */
    // int update(Recurrence recurrence);
    
    // /**
    //  * 更新下一次发生时间
    //  */
    // int updateNextTime(Long taskId, LocalDateTime nextTime);
    
    // /**
    //  * 更新重复次数
    //  */
    // int updateCount(Long taskId, Integer count);
    
    // /**
    //  * 删除循环任务配置
    //  */
    // int deleteByTaskId(Long taskId);
    
    // /**
    //  * 查询用户即将发生的循环任务
    //  */
    // List<Recurrence> getUpcomingByUserId(Long userId, LocalDateTime deadline);
}