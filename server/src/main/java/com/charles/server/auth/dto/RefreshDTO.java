package com.charles.server.auth.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class RefreshDTO {
    @NotBlank(message = "Refresh token is required")
    private String refreshToken;
}