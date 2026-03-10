package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TagDeleteRequest {
    @NotNull(message = "tagId is required")
    private Long tagId;
}