package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class CreateTaskTagRequest {
    @NotBlank(message = "Task ID is Required")
    private Long taskId;

    @NotBlank(message = "Tag ID is Required")
    private Long tagId;
}