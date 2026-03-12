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
    private Boolean isRecurring = false; // DEFAULT FALSE
    
    // 状态字段（新设计）
    private Boolean isCompleted = false; // 是否完成
    private Boolean isAbandoned = false; // 是否废弃
    private Boolean isSkipped = false; // 是否跳过（仅对循环任务有效）
    
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
