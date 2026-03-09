package com.charles.server.reminder.dto;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class TaskCreateRequest {
    // task config
    private Long projectId;
    private String title;
    private Long parentTaskId;
    private LocalDateTime dueDate;
    private LocalDateTime startDate;
    private LocalDateTime reminderSentAt;
    private String priority;
    private Boolean isRecurring;
    // recurrence config
    private String recurrenceCategory;
    private Integer recurrenceInterval;
    private Integer recurrenceCount;
    private LocalDateTime recurrenceNextTime;
    private String recurrenceSchedule;
}
