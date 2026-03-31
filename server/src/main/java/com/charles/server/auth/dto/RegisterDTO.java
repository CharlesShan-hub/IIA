package com.charles.server.auth.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
@Schema(description = "User registration request data")
public class RegisterDTO {

    @NotBlank(message = "Email is required")
    @Email(message = "Email format is invalid")
    @Schema(
        description = "User email address",
        example = "{{email}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String email;

    @NotBlank(message = "Init password is required")
    @Size(min = 6, max = 20, message = "Password length must be 6-20 characters")
    @Schema(
        description = "User password",
        example = "{{password}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String password;

    @NotBlank(message = "verification code is required")
    @Schema(
        description = "Verification code sent to email, if app is dev environment, this code is returned to client.",
        example = "{{code}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String code;

    @Size(min=1, max = 20, message = "Username length must be 1-20 characters")
    @Schema(
        description = "User display name",
        example = "{{username}}"
    )
    private String username;
}