package com.charles.server.auth.entity;

import lombok.Data;

@Data
public class Account {
    private Long userId;
    private String passwordHash;
}