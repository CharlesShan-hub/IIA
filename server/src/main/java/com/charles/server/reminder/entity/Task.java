package com.charles.server.reminder.entity;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class Task {
    private Long taskId; // AUTO_INCREMENT
    private Long userId; // NOT NULL
    private Long projectId; // NULL
    
    // 核心元数据
    private String title; // NOT NULL
    private String category; // 'task' 或 'note' NOT NULL DEFAULT 'task'
    private String status; // 'todo', 'done' 或 'abandoned' NOT NULL DEFAULT 'todo'
    private Boolean isArchived; // DEFAULT FALSE
    
    // 层级结构
    private Long parentTaskId; // NULL
    private Integer sortOrder;
    
    // 时间信息
    private LocalDateTime dueDate;
    private LocalDateTime startDate;
    private LocalDateTime completedAt;
    private LocalDateTime reminderSentAt;
    
    // 优先级
    private String priority; // 'none', 'low', 'medium', 'high'
}
