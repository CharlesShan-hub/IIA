package com.charles.server.utils;

import java.util.HashMap;
import java.util.Map;

/**
 * Response formatting utility to standardize API responses.
 */
public class ResponseUtils {
    
    /**
     * Build a successful response.
     * @param data response payload
     * @param message response message
     * @return formatted response map
     */
    public static Map<String, Object> buildSuccessResponse(Object data, String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("code", 200);
        response.put("msg", message);
        response.put("data", data);
        return response;
    }
    
    /**
     * Build a successful response with the default message.
     * @param data response payload
     * @return formatted response map
     */
    public static Map<String, Object> buildSuccessResponse(Object data) {
        return buildSuccessResponse(data, "success");
    }
    
    /**
     * Build a successful response without data.
     * @param message response message
     * @return formatted response map
     */
    public static Map<String, Object> buildEmptySuccessResponse(String message) {
        return buildSuccessResponse(null, message);
    }
    
    /**
     * Build an error response.
     * @param code error code
     * @param message error message
     * @return formatted error response map
     */
    public static Map<String, Object> buildErrorResponse(int code, String message) {
        Map<String, Object> errorResponse = new HashMap<>();
        errorResponse.put("code", code);
        errorResponse.put("msg", message);
        errorResponse.put("data", null);
        return errorResponse;
    }
    
    /**
     * Build a default error response (code 400).
     * @param message error message
     * @return formatted error response map
     */
    public static Map<String, Object> buildErrorResponse(String message) {
        return buildErrorResponse(400, message);
    }
    
    /**
     * Build an unauthorized response (code 401).
     * @param message error message
     * @return formatted error response map
     */
    public static Map<String, Object> buildUnauthorizedResponse(String message) {
        return buildErrorResponse(401, message);
    }
}