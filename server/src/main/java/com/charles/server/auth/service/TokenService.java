package com.charles.server.auth.service;

import jakarta.servlet.http.HttpServletRequest;

public interface TokenService {
    /**
     * Store AccessToken to Redis with expiration time
     * @param userId user id
     * @param token JWT Access Token
     */
    void storeAccessToken(String userId, String token);
    
    /**
     * Store RefreshToken to Redis with expiration time
     * @param userId user id
     * @param refreshToken JWT Refresh Token
     */
    void storeRefreshToken(String userId, String refreshToken);
    
    /**
     * Get AccessToken from Redis
     * @param userId user id
     * @return Access Token
     */
    String getAccessToken(String userId);
    
    /**
     * Get RefreshToken from Redis
     * @param userId user id
     * @return Refresh Token
     */
    String getRefreshToken(String userId);

    /**
     * Delete all tokens (user logout)
     * @param userId user id
     */
    void delete(String userId);
    
    /**
     * Validate AccessToken
     * @param userId user id
     * @param token JWT Access Token
     * @return 是否有效
     */
    boolean validateAccessToken(String userId, String token);
    
    /**
     * Validate RefreshToken
     * @param userId user id
     * @param refreshToken JWT Refresh Token
     * @return 是否有效
     */
    boolean validateRefreshToken(String userId, String refreshToken);

    /**
     * Get userId from HttpServletRequest
     * @param request HTTP请求对象
     * @return 用户ID
     * @throws RuntimeException 如果认证失败
     */
    Long getUserIdFromRequest(HttpServletRequest request);
}