package com.charles.server.reminder.dto;

import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class ProjectUpdateDTO {

    @Size(min = 1, max = 20, message = "Project Name must be between 1 and 20 characters")
    private String name;

    @Size(min = 1, max = 500, message = "Project Description must be between 1 and 500 characters")
    private String description;

    private String color;
    private String icon;
    private Long userId;
    private Long projectId;
    private Boolean isArchived;
}
