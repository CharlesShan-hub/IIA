package com.charles.server.reminder.dto;

import lombok.Data;
import jakarta.validation.constraints.NotNull;

@Data
public class ProjectGetDTO {
    @NotNull(message = "archived is required")
    private Boolean archived = false;
    // true: return archived + unarchived projects
    private Boolean isAll = false;
}
