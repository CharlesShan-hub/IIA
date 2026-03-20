package com.charles.server.auth.dto;

import lombok.Data;

@Data
public class LoginVO {
    private String token;
    private String refreshToken;
    private String userId;
}
