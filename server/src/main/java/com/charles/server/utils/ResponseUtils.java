package com.charles.server.utils;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Standard API response DTO with Swagger annotations.
 * This class replaces the old utility methods while maintaining backward compatibility.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Standard API response structure")
public class ResponseUtils<T> {
    
    @Schema(
        description = "Response status code",
        example = "200",
        type = "integer",
        minimum = "100",
        maximum = "599"
    )
    private Integer code;
    
    @Schema(
        description = "Response message",
        example = "success",
        type = "string"
    )
    private String msg;
    
    @Schema(
        description = "Response data payload, can be null for error responses",
        nullable = true
    )
    private T data;
    
    /**
     * Build a successful response.
     * @param data response payload
     * @param message response message
     * @return formatted response
     */
    public static <T> ResponseUtils<T> buildSuccessResponse(T data, String message) {
        return new ResponseUtils<>(200, message, data);
    }
    
    /**
     * Build a successful response with the default message.
     * @param data response payload
     * @return formatted response
     */
    public static <T> ResponseUtils<T> buildSuccessResponse(T data) {
        return buildSuccessResponse(data, "success");
    }
    
    /**
     * Build a successful response without data.
     * @param message response message
     * @return formatted response
     */
    public static <T> ResponseUtils<T> buildEmptySuccessResponse(String message) {
        return buildSuccessResponse(null, message);
    }
    
    /**
     * Build an error response.
     * @param code error code
     * @param message error message
     * @return formatted error response
     */
    public static <T> ResponseUtils<T> buildErrorResponse(int code, String message) {
        return new ResponseUtils<>(code, message, null);
    }
    
    /**
     * Build a default error response (code 400).
     * @param message error message
     * @return formatted error response
     */
    public static <T> ResponseUtils<T> buildErrorResponse(String message) {
        return buildErrorResponse(400, message);
    }
    
    /**
     * Build an unauthorized response (code 401).
     * @param message error message
     * @return formatted error response
     */
    public static <T> ResponseUtils<T> buildUnauthorizedResponse(String message) {
        return buildErrorResponse(401, message);
    }

    public static <T> ResponseUtils<T> buildForbiddenResponse(String message) {
        return buildErrorResponse(403, message);
    }

    public static <T> ResponseUtils<T> buildNotFoundResponse(String message) {
        return buildErrorResponse(404, message);
    }

    public static <T> ResponseUtils<T> buildConflictResponse(String message) {
        return buildErrorResponse(409, message);
    }

    public static <T> ResponseUtils<T> buildUnprocessableResponse(String message) {
        return buildErrorResponse(422, message);
    }

    public static <T> ResponseUtils<T> buildServerErrorResponse(String message) {
        return buildErrorResponse(500, message);
    }

    public static <T> ResponseUtils<T> buildResponse(int code, String message, T data) {
        return new ResponseUtils<>(code, message, data);
    }

    public static <T> ResponseUtils<T> buildSuccess() {
        return buildSuccessResponse(null, "success");
    }

    public static <T> ResponseUtils<T> buildCreatedResponse(T data) {
        return buildResponse(201, "created", data);
    }

    public static <T> ResponseUtils<T> buildUpdatedResponse(T data) {
        return buildResponse(200, "updated", data);
    }

    public static <T> ResponseUtils<T> buildDeletedResponse() {
        return buildResponse(200, "deleted", null);
    }

    public static <T> ResponseUtils<T> buildPageResponse(T items, long total, int page, int size) {
        // Create a wrapper object for paginated data
        // Note: This method signature needs to be adjusted based on your pagination structure
        return buildSuccessResponse(items, "success");
    }
}