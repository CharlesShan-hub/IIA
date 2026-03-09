package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import lombok.Data;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TaskStatusUpdateRequest {
    @NotNull(message = "taskId is required")
    private Long taskId;

    @NotBlank(message = "status is required")
    @Pattern(regexp = "^(done|todo|abandoned)$", message = "status must be one of: done|todo|abandoned")
    private String status; // expected: "done" | "todo" | "abandoned"

    // optional: when true, apply status to all descendants
    private Boolean cascade = Boolean.FALSE;

    public TaskStatusUpdateRequest(Long taskId, String status) {
        this.taskId = taskId;
        this.status = status;
        this.cascade = Boolean.FALSE;
    }
}