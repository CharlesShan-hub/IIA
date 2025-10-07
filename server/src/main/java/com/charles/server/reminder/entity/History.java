package com.charles.server.reminder.entity;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class History {
    private Long historyId; // 历史记录ID
    private Long taskId; // 任务ID
    private LocalDateTime dueDate; // 任务截止日期
    private LocalDateTime startDate; // 任务开始日期
    private LocalDateTime completedAt; // 任务完成日期
    private LocalDateTime reminderSentAt; // 提醒已发送时间
    private Integer current; // 当前重复次数, 从1开始
    private String status; // 'todo', 'done', 'skipped', 'abandoned'
}