package com.charles.server.iia.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

/**
 * Token管理服务，用于在Redis中存储和验证Token
 */
@Service
public class TokenService {
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    /**
     * 存储Token到Redis，设置过期时间
     * @param userId 用户ID
     * @param token JWT Token
     */
    public void storeToken(String userId, String token) {
        String key = "user:token:" + userId;
        redisTemplate.opsForValue().set(key, token, 24, TimeUnit.HOURS);
    }
    
    /**
     * 从Redis获取Token
     * @param userId 用户ID
     * @return Token
     */
    public String getToken(String userId) {
        String key = "user:token:" + userId;
        return redisTemplate.opsForValue().get(key);
    }
    
    /**
     * 从Redis删除Token（用户登出）
     * @param userId 用户ID
     */
    public void deleteToken(String userId) {
        String key = "user:token:" + userId;
        redisTemplate.delete(key);
    }
    
    /**
     * 验证Token是否有效
     * @param userId 用户ID
     * @param token JWT Token
     * @return 是否有效
     */
    public boolean validateToken(String userId, String token) {
        String storedToken = getToken(userId);
        return storedToken != null && storedToken.equals(token);
    }
}