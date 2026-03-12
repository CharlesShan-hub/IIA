package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TaskUpdateAbandonedRequest {
    @NotNull(message = "taskId is required")
    private Long taskId;

    @NotNull(message = "isAbandoned is required")
    private Boolean isAbandoned;
}