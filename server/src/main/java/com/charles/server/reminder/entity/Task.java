package com.charles.server.reminder.entity;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class Task {
    private Long taskId;
    private Long userId;
    private Long projectId;
    
    // 核心元数据
    private String title;
    private String category; // 'task' 或 'note'
    private String status; // 'todo', 'done', 'abandoned'
    
    // 层级结构
    private Long parentTaskId;
    private Double sortOrder;
    
    // 时间信息
    private LocalDateTime dueDate;
    private LocalDateTime startDate;
    private LocalDateTime completedAt;
    private LocalDateTime reminderSentAt;
    
    // 优先级
    private String priority; // 'none', 'low', 'medium', 'high'
}