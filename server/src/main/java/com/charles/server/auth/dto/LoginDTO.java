package com.charles.server.auth.dto;

import lombok.Data;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import io.swagger.v3.oas.annotations.media.Schema;

@Data
@Schema(description = "Login request data")
public class LoginDTO {
    @NotBlank(message = "email is required")
    @Email(message = "email format is incorrect")
    @Schema(
        description = "User email address",
        defaultValue = "charles.shht@gmail.com",
        example = "charles.shht@gmail.com",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String email;

    @NotBlank(message = "password is required")
    @Size(min = 6, max = 20, message = "password length must be between 6 and 20")
    @Schema(
        description = "User password",
        defaultValue = "263513",
        example = "263513",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String password;
}