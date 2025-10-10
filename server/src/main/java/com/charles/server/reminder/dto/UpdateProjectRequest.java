package com.charles.server.reminder.dto;

import com.charles.server.utils.ColorUtils;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class UpdateProjectRequest {
    @NotBlank(message = "项目名称不能为空")
    @Size(min = 1, max = 20, message = "项目名称不能超过20个字符")
    private String name;

    @Size(min = 1, max = 500, message = "项目简介不能超过500个字符")
    private String description;

    private String color;
    private String icon;
    private Long userId;
    private Long projectId;

    public void setColor(String color) {
        this.color = ColorUtils.getColorOrDefault(color, "#409EFF");
    }
}