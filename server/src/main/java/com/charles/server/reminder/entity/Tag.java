package com.charles.server.reminder.entity;

import lombok.Data;
import lombok.Builder;

@Data
@Builder
public class Tag {
    private Long tagId;
    private Long userId;
    private String name;
    private String color;
    private Long operationId;
}