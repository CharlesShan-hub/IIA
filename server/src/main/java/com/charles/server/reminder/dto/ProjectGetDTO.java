package com.charles.server.reminder.dto;

import lombok.Data;
import jakarta.validation.constraints.NotNull;
import io.swagger.v3.oas.annotations.media.Schema;

@Data
@Schema(description = "Project query request data")
public class ProjectGetDTO {
    @NotNull(message = "archived is required")
    @Schema(
        description = "Whether to query archived projects",
        example = "false",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Boolean archived = false;

    @Schema(
        description = "Whether to return both archived and unarchived projects",
        example = "false"
    )
    private Boolean isAll = false;
}
