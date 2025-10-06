package com.charles.server.auth.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class RegisterResponse {
    private Long userId;
    private String passwordHash;
    private String token;
}