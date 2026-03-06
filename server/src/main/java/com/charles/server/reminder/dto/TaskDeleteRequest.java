package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TaskDeleteRequest {
    @NotNull(message = "taskId is required")
    private Long taskId;
}
