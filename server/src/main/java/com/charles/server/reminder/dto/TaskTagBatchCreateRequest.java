package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.util.List;

@Data
public class TaskTagBatchCreateRequest {
    @NotNull(message = "Task ID is Required")
    private Long taskId;

    @NotNull(message = "Tag IDs are Required")
    private List<Long> tagIds;

    private Boolean includeSubtasks;
}