package com.charles.server.iia.auth.utils;

import org.springframework.util.StringUtils;

import jakarta.servlet.http.HttpServletRequest;

/**
 * Token 相关的工具方法，用于处理 Token 的提取、格式化等操作
 */
public class TokenUtils {
    
    /**
     * 从请求头中提取 JWT Token
     * @param request HTTP请求对象
     * @return 提取的Token，如果不存在或格式不正确则返回null
     */
    public static String getTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        throw new RuntimeException("未提供有效的认证 Token");
        // return null;
    }
}