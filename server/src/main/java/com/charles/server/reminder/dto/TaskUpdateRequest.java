package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TaskUpdateRequest {
    @NotNull(message = "taskId is required")
    private Long taskId;

    private Long projectId;
    private String title;
    private Boolean isRecurring;
    private Long parentTaskId;

    private java.time.LocalDateTime dueDate;
    private java.time.LocalDateTime startDate;
    private java.time.LocalDateTime completedAt;
    private java.time.LocalDateTime reminderSentAt;

    private String priority;

    private String recurrenceCategory;
    private Integer recurrenceInterval;
    private Integer recurrenceCount;
    private java.time.LocalDateTime recurrenceNextTime;
    private String recurrenceSchedule;
}