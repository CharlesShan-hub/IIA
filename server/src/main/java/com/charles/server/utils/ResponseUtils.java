package com.charles.server.utils;

import java.util.HashMap;
import java.util.Map;

/**
 * 响应格式化工具类，用于统一API响应格式
 */
public class ResponseUtils {
    
    /**
     * 构建成功响应
     * @param data 响应数据
     * @param message 响应消息
     * @return 格式化后的响应Map
     */
    public static Map<String, Object> buildSuccessResponse(Object data, String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("code", 200);
        response.put("msg", message);
        response.put("data", data);
        return response;
    }
    
    /**
     * 构建成功响应（使用默认消息）
     * @param data 响应数据
     * @return 格式化后的响应Map
     */
    public static Map<String, Object> buildSuccessResponse(Object data) {
        return buildSuccessResponse(data, "success");
    }
    
    /**
     * 构建空数据的成功响应
     * @param message 响应消息
     * @return 格式化后的响应Map
     */
    public static Map<String, Object> buildEmptySuccessResponse(String message) {
        return buildSuccessResponse(null, message);
    }
    
    /**
     * 构建错误响应
     * @param code 错误代码
     * @param message 错误消息
     * @return 格式化后的错误响应Map
     */
    public static Map<String, Object> buildErrorResponse(int code, String message) {
        Map<String, Object> errorResponse = new HashMap<>();
        errorResponse.put("code", code);
        errorResponse.put("msg", message);
        errorResponse.put("data", null);
        return errorResponse;
    }
    
    /**
     * 构建默认错误响应（错误代码为400）
     * @param message 错误消息
     * @return 格式化后的错误响应Map
     */
    public static Map<String, Object> buildErrorResponse(String message) {
        return buildErrorResponse(400, message);
    }
    
    /**
     * 构建认证失败响应（错误代码为401）
     * @param message 错误消息
     * @return 格式化后的错误响应Map
     */
    public static Map<String, Object> buildUnauthorizedResponse(String message) {
        return buildErrorResponse(401, message);
    }
}