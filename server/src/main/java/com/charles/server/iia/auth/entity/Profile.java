package com.charles.server.iia.auth.entity;

import java.time.LocalDateTime;

import lombok.Data;

@Data
public class Profile {
    private Long userId;
    private String username;
    private LocalDateTime createdAt;
}