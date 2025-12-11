package com.charles.server.auth.entity;

import lombok.Data;

@Data
public class Mail {
    private String email;
    private Long userId;
}