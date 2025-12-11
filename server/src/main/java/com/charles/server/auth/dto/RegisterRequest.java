package com.charles.server.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class RegisterRequest {

    @NotBlank(message = "Email is required")
    @Email(message = "Email format is invalid")
    private String email;

    @NotBlank(message = "Init password is required")
    @Size(min = 6, max = 20, message = "Password length must be 6-20 characters")
    private String password;

    @NotBlank(message = "verification code is required")
    private String code;

    @Size(min=1, max = 20, message = "Username length must be 1-20 characters")
    private String username;
}