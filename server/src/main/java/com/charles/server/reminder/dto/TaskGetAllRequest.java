package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TaskGetAllRequest {
    @NotNull(message = "isAll is required")
    private Boolean isAll = false;
    private Long projectId;
}
