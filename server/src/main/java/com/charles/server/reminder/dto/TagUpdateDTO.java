package com.charles.server.reminder.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;
import io.swagger.v3.oas.annotations.media.Schema;

@Data
@Schema(description = "Tag update request data")
public class TagUpdateDTO {
    @NotNull(message = "Tag ID is Required")
    @Schema(
        description = "Tag ID",
        example = "1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Long tagId;

    @Size(min = 1, max = 20, message = "Tag Name must be between 1 and 20 characters")
    @Pattern(regexp = "^(?!\\s*$).+", message = "Tag Name cannot be blank")
    @Schema(
        description = "Tag name",
        example = "Work",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String name;

    @Schema(
        description = "Tag color",
        example = "#409EFF",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String color;

    public void setColor(String color) {
        this.color = (color == null || color.trim().isEmpty()) ? null : color;
    }
}
