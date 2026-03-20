package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TaskUpdateCompletedDTO {
    @NotNull(message = "taskId is required")
    private Long taskId;

    @NotNull(message = "isCompleted is required")
    private Boolean isCompleted;
}