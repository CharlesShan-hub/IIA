package com.charles.server.reminder.dto;

import com.charles.server.utils.ColorUtils;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;
import io.swagger.v3.oas.annotations.media.Schema;

@Data
@Schema(description = "Tag create request data")
public class TagCreateDTO {
    @NotBlank(message = "Tag Name is Required")
    @Size(min = 1, max = 20, message = "Tag Name must be between 1 and 20 characters")
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
        this.color = ColorUtils.getColorOrDefault(color, "#409EFF");
    }
}
