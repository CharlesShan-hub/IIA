package com.charles.server.iia.auth.service;

import jakarta.servlet.http.HttpServletRequest;

/**
 * Token管理服务接口，定义Token操作的核心方法
 */
public interface TokenService {
    /**
     * 存储AccessToken到Redis，设置过期时间
     * @param userId 用户ID
     * @param token JWT Access Token
     */
    void storeAccessToken(String userId, String token);
    
    /**
     * 存储RefreshToken到Redis，设置过期时间
     * @param userId 用户ID
     * @param refreshToken JWT Refresh Token
     */
    void storeRefreshToken(String userId, String refreshToken);
    
    /**
     * 从Redis获取AccessToken
     * @param userId 用户ID
     * @return Access Token
     */
    String getAccessToken(String userId);
    
    /**
     * 从Redis获取RefreshToken
     * @param userId 用户ID
     * @return Refresh Token
     */
    String getRefreshToken(String userId);
    
    /**
     * 从Redis删除AccessToken（用户登出）
     * @param userId 用户ID
     */
    void deleteAccessToken(String userId);
    
    /**
     * 从Redis删除RefreshToken（用户登出）
     * @param userId 用户ID
     */
    void deleteRefreshToken(String userId);
    
    /**
     * 删除用户的所有Token（用户登出）
     * @param userId 用户ID
     */
    void deleteAllTokens(String userId);
    
    /**
     * 验证AccessToken是否有效
     * @param userId 用户ID
     * @param token JWT Access Token
     * @return 是否有效
     */
    boolean validateAccessToken(String userId, String token);
    
    /**
     * 验证RefreshToken是否有效
     * @param userId 用户ID
     * @param refreshToken JWT Refresh Token
     * @return 是否有效
     */
    boolean validateRefreshToken(String userId, String refreshToken);
    
    /**
     * 通过AccessToken获取用户ID
     * @param accessToken JWT Access Token
     * @return 用户ID
     */
    Long getUserIdByAccessToken(String accessToken);
    
    /**
     * 从请求头中提取 JWT Token
     * @param request HTTP请求对象
     * @return 提取的Token
     * @throws RuntimeException 如果不存在或格式不正确
     */
    String extractTokenFromRequest(HttpServletRequest request);
    
    /**
     * 从请求中获取用户ID
     * @param request HTTP请求对象
     * @return 用户ID
     * @throws RuntimeException 如果认证失败
     */
    Long getUserIdFromRequest(HttpServletRequest request);
}