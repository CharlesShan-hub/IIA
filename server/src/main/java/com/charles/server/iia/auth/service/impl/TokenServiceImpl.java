package com.charles.server.iia.auth.service.impl;

import java.util.concurrent.TimeUnit;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import com.charles.server.iia.auth.service.TokenService;
import com.charles.server.iia.auth.utils.JwtUtils;

import jakarta.servlet.http.HttpServletRequest;

/**
 * Token管理服务实现类，负责在Redis中存储和验证Token
 */
@Service
public class TokenServiceImpl implements TokenService {
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    @Autowired
    private JwtUtils jwtUtils;
    
    // Token过期时间：24小时
    private static final long TOKEN_EXPIRATION = 24;
    
    // Refresh Token过期时间：7天
    private static final long REFRESH_TOKEN_EXPIRATION = 7 * 24;
    
    @Override
    public void storeAccessToken(String userId, String token) {
        String key = "user:access_token:" + userId;
        redisTemplate.opsForValue().set(key, token, TOKEN_EXPIRATION, TimeUnit.HOURS);
        
        // 添加反向映射：accessToken -> userId
        String reverseKey = "access_token:user_id:" + token;
        redisTemplate.opsForValue().set(reverseKey, userId, TOKEN_EXPIRATION, TimeUnit.HOURS);
    }
    
    @Override
    public void storeRefreshToken(String userId, String refreshToken) {
        String key = "user:refresh_token:" + userId;
        redisTemplate.opsForValue().set(key, refreshToken, REFRESH_TOKEN_EXPIRATION, TimeUnit.HOURS);
    }
    
    @Override
    public String getAccessToken(String userId) {
        String key = "user:access_token:" + userId;
        return redisTemplate.opsForValue().get(key);
    }
    
    @Override
    public String getRefreshToken(String userId) {
        String key = "user:refresh_token:" + userId;
        return redisTemplate.opsForValue().get(key);
    }
    
    @Override
    public void deleteAccessToken(String userId) {
        String key = "user:access_token:" + userId;
        String token = redisTemplate.opsForValue().get(key);
        
        // 删除正向映射
        redisTemplate.delete(key);
        
        // 如果存在Token，同时删除反向映射
        if (token != null) {
            String reverseKey = "access_token:user_id:" + token;
            redisTemplate.delete(reverseKey);
        }
    }
    
    @Override
    public void deleteRefreshToken(String userId) {
        String key = "user:refresh_token:" + userId;
        redisTemplate.delete(key);
    }
    
    @Override
    public void deleteAllTokens(String userId) {
        deleteAccessToken(userId);
        deleteRefreshToken(userId);
    }
    
    @Override
    public boolean validateAccessToken(String userId, String token) {
        // 从Redis中获取存储的Token
        String storedToken = getAccessToken(userId);
        // 验证传入的Token是否与Redis中存储的一致
        return storedToken != null && storedToken.equals(token);
    }
    
    @Override
    public boolean validateRefreshToken(String userId, String refreshToken) {
        String storedRefreshToken = getRefreshToken(userId);
        return storedRefreshToken != null && storedRefreshToken.equals(refreshToken);
    }
    
    @Override
    public Long getUserIdByAccessToken(String accessToken) {
        // 从反向映射中获取用户ID
        String key = "access_token:user_id:" + accessToken;
        String userIdStr = redisTemplate.opsForValue().get(key);
        return userIdStr != null ? Long.parseLong(userIdStr) : null;
    }
    
    @Override
    public String extractTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        throw new RuntimeException("未提供有效的认证 Token");
    }
    
    @Override
    public Long getUserIdFromRequest(HttpServletRequest request) {
        String token = extractTokenFromRequest(request);
        String userId = jwtUtils.getUserIdFromToken(token);
        return Long.valueOf(userId);
    }
}