package com.charles.server.auth.dto;

import lombok.Data;

@Data
public class RegisterResponse {
    private Long userId;
    private String token;
    private String refreshToken;
}