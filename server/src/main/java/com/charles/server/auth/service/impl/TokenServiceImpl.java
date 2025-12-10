package com.charles.server.auth.service.impl;

import java.util.concurrent.TimeUnit;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import com.charles.server.auth.service.TokenService;
import com.charles.server.utils.JwtUtils;

import jakarta.servlet.http.HttpServletRequest;

@Service
public class TokenServiceImpl implements TokenService {
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    @Autowired
    private JwtUtils jwtUtils;

    @Value("${jwt.expiration}")
    private long tokenExpiration;
    
    @Value("${jwt.refresh-expiration}")
    private long refreshTokenExpiration;

    @Override
    public void storeAccessToken(String userId, String token) {
        String key = "user:access_token:" + userId;
        redisTemplate.opsForValue().set(key, token, tokenExpiration, TimeUnit.HOURS);
        
        // Add reverse mapping: accessToken -> userId
        String reverseKey = "access_token:user_id:" + token;
        redisTemplate.opsForValue().set(reverseKey, userId, tokenExpiration, TimeUnit.HOURS);
    }
    
    @Override
    public void storeRefreshToken(String userId, String refreshToken) {
        String key = "user:refresh_token:" + userId;
        redisTemplate.opsForValue().set(key, refreshToken, refreshTokenExpiration, TimeUnit.HOURS);
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
        redisTemplate.delete(key);
        if (token != null) {
            // if the token exists, delete the reverse mapping
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
        // Retrieve the stored token from Redis
        String storedToken = getAccessToken(userId);
        // Verify that the provided token matches the one stored in Redis
        return storedToken != null && storedToken.equals(token);
    }
    
    @Override
    public boolean validateRefreshToken(String userId, String refreshToken) {
        String storedRefreshToken = getRefreshToken(userId);
        return storedRefreshToken != null && storedRefreshToken.equals(refreshToken);
    }
    
    @Override
    public Long getUserIdByAccessToken(String accessToken) {
        // Retrieve the user ID from the reverse mapping
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
        throw new RuntimeException("No valid Authorization header found");
    }
    
    @Override
    public Long getUserIdFromRequest(HttpServletRequest request) {
        String token = extractTokenFromRequest(request);
        String userId = jwtUtils.getUserIdFromToken(token);
        return Long.valueOf(userId);
    }
}