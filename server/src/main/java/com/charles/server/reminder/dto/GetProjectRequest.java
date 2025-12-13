package com.charles.server.reminder.dto;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;

@Data
public class GetProjectRequest {
    @NotBlank(message = "projectId is required")
    private Long projectId;
}
