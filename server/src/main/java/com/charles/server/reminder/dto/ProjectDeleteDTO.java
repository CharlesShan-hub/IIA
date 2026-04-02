package com.charles.server.reminder.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Project delete request data")
public class ProjectDeleteDTO {
    @NotNull(message = "projectId is required")
    @Schema(
        description = "Project ID",
        example = "1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Long projectId;
    
    @NotNull(message = "keepTasks is required")
    @Schema(
        description = "Keep tasks when deleting the project",
        example = "true",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    @Builder.Default
    private Boolean keepTasks = Boolean.TRUE;

    @Schema(
        description = "Delete the target project",
        example = "false",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    @Builder.Default
    private Boolean targetProject = Boolean.FALSE;

    @Schema(
        description = "Target project ID",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Long targetProjectId;
}
