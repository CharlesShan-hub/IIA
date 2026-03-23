package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProjectDeleteDTO {
    @NotNull(message = "projectId is required")
    private Long projectId;
    
    @NotNull(message = "keepTasks is required")
    @Builder.Default
    private Boolean keepTasks = Boolean.TRUE;

    @Builder.Default
    private Boolean targetProject = Boolean.FALSE;

    private Long targetProjectId;
}
