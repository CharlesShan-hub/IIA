package com.charles.server.auth.service.impl;

import java.util.concurrent.TimeUnit;

import com.charles.server.auth.exception.TokenException;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import java.util.Objects;

import com.charles.server.auth.service.TokenService;
import com.charles.server.utils.JwtUtils;

import jakarta.servlet.http.HttpServletRequest;

@Service
@RequiredArgsConstructor
public class TokenServiceImpl implements TokenService {

    private final RedisTemplate<String, String> redisTemplate;
    private final JwtUtils jwtUtils;

    @Value("${jwt.expiration}")
    private long tokenExpiration;
    
    @Value("${jwt.refresh-expiration}")
    private long refreshTokenExpiration;

    @Override
    public void storeAccessToken(String userId, String token) {
        String key = "user:access_token:" + userId;
        redisTemplate.opsForValue().set(key, Objects.requireNonNull(token), tokenExpiration, TimeUnit.HOURS);
        
        // Add reverse mapping: accessToken -> userId
        String reverseKey = "access_token:user_id:" + Objects.requireNonNull(token);
        redisTemplate.opsForValue().set(reverseKey, Objects.requireNonNull(userId), tokenExpiration, TimeUnit.HOURS);
    }
    
    @Override
    public void storeRefreshToken(String userId, String refreshToken) {
        String key = "user:refresh_token:" + userId;
        redisTemplate.opsForValue().set(key, Objects.requireNonNull(refreshToken), refreshTokenExpiration, TimeUnit.HOURS);
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

    private void deleteAccessToken(String userId) {
        String key = "user:access_token:" + userId;
        String token = redisTemplate.opsForValue().get(key);
        redisTemplate.delete(key);
        if (token != null) {
            // if the token exists, delete the reverse mapping
            String reverseKey = "access_token:user_id:" + token;
            redisTemplate.delete(reverseKey);
        }
    }

    private void deleteRefreshToken(String userId) {
        String key = "user:refresh_token:" + userId;
        redisTemplate.delete(key);
    }

    public void delete(String userId) {
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

    private String extractTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        throw TokenException.invalid("Invalid Bearer Token");
    }
    
    @Override
    public Long getUserIdFromRequest(HttpServletRequest request) {
        String token = extractTokenFromRequest(request);
        String userId = jwtUtils.getUserIdFromToken(token);
        return Long.valueOf(userId);
    }
}