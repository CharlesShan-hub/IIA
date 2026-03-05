package com.charles.server.auth.service;

import jakarta.servlet.http.HttpServletRequest;

import java.util.Map;

public interface TokenService {

    /**
     * Refresh tokens using refresh token
     * @param token JWT Refresh Token
     * @return New Tokens (accessToken, refreshToken)
     */
    Map<String, String> refresh(String token);

    /**
     * Generate, store and get tokens
     */
    Map<String, String> get(String userId);

    /**
     * Delete all tokens (user logout)
     */
    void delete(String userId);
    
    /**
     * Get userId from HttpServletRequest
     * @param request HTTP请求对象
     * @return 用户ID
     * @throws RuntimeException 如果认证失败
     */
    Long getUserIdFromRequest(HttpServletRequest request);
}