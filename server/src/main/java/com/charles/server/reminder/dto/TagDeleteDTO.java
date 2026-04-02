package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import io.swagger.v3.oas.annotations.media.Schema;

@Data
@Schema(description = "Tag delete request data")
public class TagDeleteDTO {
    @NotNull(message = "tagId is required")
    @Schema(
        description = "Tag ID",
        example = "1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Long tagId;
}