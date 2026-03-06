package com.charles.server.reminder.dto;

import com.charles.server.utils.ColorUtils;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class TagUpdateRequest {
    @NotBlank(message = "Tag ID is Required")
    private Long tagId;

    @NotBlank(message = "Tag Name is Required")
    @Size(min = 1, max = 20, message = "Tag Name must be between 1 and 20 characters")
    private String name;

    private String color;

    public void setColor(String color) {
        this.color = ColorUtils.getColorOrDefault(color, "#409EFF");
    }
}
