package com.charles.server.reminder.entity;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class Project {
    private Long projectId;
    private Long userId;
    private String name;
    private String description;
    private String color;
    private String icon;
    private Integer sortOrder;
    private Boolean isArchived;
    private Long operationId;
}