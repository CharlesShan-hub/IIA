package com.charles.server.reminder.entity;

import java.time.LocalDateTime;
import com.charles.server.reminder.dto.CreateTaskRequest;
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

    public Task() {
    }

    public Task(CreateTaskRequest dto) {
        this.userId = dto.getUserId();
        this.projectId = dto.getProjectId();
        this.title = dto.getTitle();
        this.category = dto.getCategory();
        this.parentTaskId = dto.getParentTaskId();
        this.dueDate = dto.getDueDate();
        this.startDate = dto.getStartDate();
        this.reminderSentAt = dto.getReminderSentAt();
        this.priority = dto.getPriority();
    }
}