package com.charles.server.auth.dto;

import lombok.Data;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Data
public class LoginRequest {
    @NotBlank(message = "email is required")
    @Email(message = "email format is incorrect")
    private String email;

    @NotBlank(message = "password is required")
    @Size(min = 6, max = 20, message = "password length must be between 6 and 20")
    private String password;
}