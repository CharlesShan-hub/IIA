package com.charles.server.auth.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Refresh token request DTO
 * <p>
 * Note: The example value uses Postman-style variable syntax {{refresh_token}}.
 * In Postman, set the 'refresh_token' environment variable to use this.
 * </p>
 */
@Data
@Schema(description = "Refresh token request DTO")
public class RefreshDTO {
    @Schema(
        description = "Refresh token for getting new access token. Format: JWT token.\n" +
                     "Note: Uses Postman variable syntax {{refreshToken}}. Set this variable in Postman.",
        example = "{{refreshToken}}",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    @NotBlank(message = "Refresh token is required")
    private String refreshToken;
}