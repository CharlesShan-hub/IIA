package com.charles.server.reminder.dto;

import com.charles.server.utils.ColorUtils;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
@Schema(description = "Project create request data")
public class ProjectCreateDTO {
    @NotBlank(message = "Project Name is Required")
    @Size(min = 1, max = 20, message = "Project Name must be between 1 and 20 characters")
    @Schema(
        description = "Project name",
        example = "P1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String name;

    @Size(min = 1, max = 500, message = "Project Description must be between 1 and 500 characters")
    @Schema(
        description = "Project description",
        example = "Project 1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String description;

    @Schema(
        description = "Project color",
        example = "#409EFF",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String color;
    
    @Schema(
        description = "Project icon",
        example = "icon-1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String icon;

    public void setColor(String color) {
        this.color = ColorUtils.getColorOrDefault(color, "#409EFF");
    }
}
