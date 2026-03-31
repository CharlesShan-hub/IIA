package com.charles.server.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Reset password request DTO")
public class ResetPasswordDTO {

    @NotBlank(message = "Email is required")
    @Email(message = "Email format is invalid")
    @Schema(
        description = "User email address",
        example = "{{email}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String email;

    @NotBlank(message = "New password is required")
    @Size(min = 6, max = 20, message = "Password length must be 6-20 characters")
    @Schema(
        description = "New password",
        example = "{{newPassword}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String newPassword;

    @NotBlank(message = "verification code is required")
    @Schema(
        description = "Verification code received via email",
        example = "{{code}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String code;
}