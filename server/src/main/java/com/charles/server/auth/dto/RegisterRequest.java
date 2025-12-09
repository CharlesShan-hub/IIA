package com.charles.server.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class RegisterRequest {
    @Email
    private String email;

    @NotBlank @Size(min = 6, max = 20)
    private String password;

    private String username;

    @NotBlank(message = "verification code is required")
    private String code;
}