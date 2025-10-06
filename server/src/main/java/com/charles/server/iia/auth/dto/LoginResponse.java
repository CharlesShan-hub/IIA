package com.charles.server.iia.auth.dto;

import lombok.Data;

@Data
public class LoginResponse {
    private String token;
    private String refreshToken;
    private String userId;
}
