package com.charles.server.reminder.dto;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class CreateTaskRequest {
    private Long userId;
    private Long projectId;
    private String title;
    private String category;
    private Long parentTaskId;
    private LocalDateTime dueDate;
    private LocalDateTime startDate;
    private LocalDateTime reminderSentAt;
    private String priority;
}
