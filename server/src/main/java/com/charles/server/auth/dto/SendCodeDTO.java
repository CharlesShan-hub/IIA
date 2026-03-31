package com.charles.server.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Send verification code request DTO")
public class SendCodeDTO {
    @NotBlank(message = "email is required")
    @Email(message = "email format is incorrect")
    @Schema(
        description = "User email address to send verification code",
        example = "{{email}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private String email;
}
