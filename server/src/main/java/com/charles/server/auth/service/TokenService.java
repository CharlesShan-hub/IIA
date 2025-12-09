package com.charles.server.auth.service;

import jakarta.servlet.http.HttpServletRequest;

public interface TokenService {
    /**
     * Store AccessToken to Redis with expiration time
     * @param userId 用户ID
     * @param token JWT Access Token
     */
    void storeAccessToken(String userId, String token);
    
    /**
     * Store RefreshToken to Redis with expiration time
     * @param userId 用户ID
     * @param refreshToken JWT Refresh Token
     */
    void storeRefreshToken(String userId, String refreshToken);
    
    /**
     * Get AccessToken from Redis
     * @param userId 用户ID
     * @return Access Token
     */
    String getAccessToken(String userId);
    
    /**
     * Get RefreshToken from Redis
     * @param userId 用户ID
     * @return Refresh Token
     */
    String getRefreshToken(String userId);
    
    /**
     * Delete AccessToken from Redis (user logout)
     * @param userId 用户ID
     */
    void deleteAccessToken(String userId);
    
    /**
     * Delete RefreshToken from Redis (user logout)
     * @param userId 用户ID
     */
    void deleteRefreshToken(String userId);
    
    /**
     * Delete all tokens (user logout)
     * @param userId 用户ID
     */
    void deleteAllTokens(String userId);
    
    /**
     * Validate AccessToken
     * @param userId 用户ID
     * @param token JWT Access Token
     * @return 是否有效
     */
    boolean validateAccessToken(String userId, String token);
    
    /**
     * Validate RefreshToken
     * @param userId 用户ID
     * @param refreshToken JWT Refresh Token
     * @return 是否有效
     */
    boolean validateRefreshToken(String userId, String refreshToken);
    
    /**
     * Get userId by AccessToken
     * @param accessToken JWT Access Token
     * @return 用户ID
     */
    Long getUserIdByAccessToken(String accessToken);
    
    /**
     * Extract JWT Token from HttpServletRequest
     * @param request HTTP请求对象
     * @return 提取的Token
     * @throws RuntimeException 如果不存在或格式不正确
     */
    String extractTokenFromRequest(HttpServletRequest request);
    
    /**
     * Get userId from HttpServletRequest
     * @param request HTTP请求对象
     * @return 用户ID
     * @throws RuntimeException 如果认证失败
     */
    Long getUserIdFromRequest(HttpServletRequest request);
}