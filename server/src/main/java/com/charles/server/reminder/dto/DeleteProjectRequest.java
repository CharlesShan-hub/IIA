package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class DeleteProjectRequest {
    @NotNull(message = "projectId is required")
    private Long projectId;
    @NotNull(message = "keepTasks is required")
    private Boolean keepTasks = Boolean.TRUE;
    @NotNull(message = "targetProject is required")
    private Boolean targetProject = Boolean.FALSE;
    @NotNull(message = "targetProjectId is required")
    private Long targetProjectId;
}