package com.charles.server.auth.entity;

import lombok.Data;

@Data
public class UserAll {
    private Long userId;
    private String passwordHash;
    private String username;
    private String email;
}