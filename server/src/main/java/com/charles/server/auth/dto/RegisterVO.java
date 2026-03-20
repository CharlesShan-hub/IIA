package com.charles.server.auth.dto;

import lombok.Data;

@Data
public class RegisterVO {
    private Long userId;
    private String token;
    private String refreshToken;
}