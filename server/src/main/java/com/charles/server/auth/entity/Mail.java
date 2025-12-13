package com.charles.server.auth.entity;

import lombok.Data;

@Data
public class Mail {
    private Long userId;
    private String email;
}