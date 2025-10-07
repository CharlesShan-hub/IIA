package com.charles.server.reminder.entity;

import lombok.Data;

@Data
public class Tag {
    private Long tagId;
    private Long userId;
    private String name;
    private String color;
}