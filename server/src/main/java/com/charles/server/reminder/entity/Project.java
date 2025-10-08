package com.charles.server.reminder.entity;

import com.charles.server.reminder.dto.CreateProjectRequest;
import lombok.Data;

@Data
public class Project {
    private Long projectId;
    private Long userId;
    private String name;
    private String description;
    private String color;
    private String icon;
    private Integer sortOrder;
    private Boolean isArchived;

    public Project() {
    }

    public Project(CreateProjectRequest dto) {
        this.name = dto.getName();
        this.description = dto.getDescription();
        this.color = dto.getColor();
        this.icon = dto.getIcon();
    }
}