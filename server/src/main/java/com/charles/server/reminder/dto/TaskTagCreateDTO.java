package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TaskTagCreateDTO {
    @NotNull(message = "Task ID is Required")
    private Long taskId;

    @NotNull(message = "Tag ID is Required")
    private Long tagId;

    private Boolean includeSubtasks;
}
