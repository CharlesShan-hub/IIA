package com.charles.server.auth.service.impl;

import java.util.Map;
import java.util.concurrent.TimeUnit;

import com.charles.server.auth.dto.RefreshResponse;
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

    private void storeAccessToken(String userId, String token) {
        String key = "token:access:user:" + userId;
        redisTemplate.opsForValue().set(key, Objects.requireNonNull(token), tokenExpiration, TimeUnit.HOURS);
        
        // Add reverse mapping: accessToken -> userId
        String reverseKey = "token:access:reverse:" + Objects.requireNonNull(token);
        redisTemplate.opsForValue().set(reverseKey, Objects.requireNonNull(userId), tokenExpiration, TimeUnit.HOURS);
    }
    
    private void storeRefreshToken(String userId, String refreshToken) {
        String key = "token:refresh:user:" + userId;
        redisTemplate.opsForValue().set(key, Objects.requireNonNull(refreshToken), refreshTokenExpiration, TimeUnit.HOURS);
        
        // Add reverse mapping: refreshToken -> userId
        String reverseKey = "token:refresh:reverse:" + Objects.requireNonNull(refreshToken);
        redisTemplate.opsForValue().set(reverseKey, Objects.requireNonNull(userId), refreshTokenExpiration, TimeUnit.HOURS);
    }
    
    private String getAccessToken(String userId) {
        String key = "token:access:user:" + userId;
        return redisTemplate.opsForValue().get(key);
    }
    
    private String getRefreshToken(String userId) {
        String key = "token:refresh:user:" + userId;
        return redisTemplate.opsForValue().get(key);
    }

    @Override
    public Map<String, String> get(String userId) {
        // Generate Tokens
        String accessToken = jwtUtils.generateAccessToken(userId);
        String refreshToken = jwtUtils.generateRefreshToken(userId);

        // Store Tokens to Redis
        storeAccessToken(userId, accessToken);
        storeRefreshToken(userId, refreshToken);

        return Map.of("accessToken", accessToken, "refreshToken", refreshToken);
    }

    private void deleteAccessToken(String userId) {
        String key = "token:access:user:" + userId;
        String token = redisTemplate.opsForValue().get(key);
        redisTemplate.delete(key);
        if (token != null) {
            // if the token exists, delete the reverse mapping
            String reverseKey = "token:access:reverse:" + token;
            redisTemplate.delete(reverseKey);
        }
    }

    private void deleteRefreshToken(String userId) {
        String key = "token:refresh:user:" + userId;
        String token = redisTemplate.opsForValue().get(key);
        redisTemplate.delete(key);
        if (token != null) {
            // if the token exists, delete the reverse mapping
            String reverseKey = "token:refresh:reverse:" + token;
            redisTemplate.delete(reverseKey);
        }
    }

    public void delete(String userId) {
        deleteAccessToken(userId);
        deleteRefreshToken(userId);
    }

    @Override
    public RefreshResponse refresh(String token) {
        // 1. Validate Refresh Token format and signature
        if (token == null || !jwtUtils.validateRefreshToken(token)) {
            throw TokenException.invalid();
        }
        
        // 2. Get user ID from token
        String userId = jwtUtils.getUserIdFromToken(token);
        
        // 3. Validate Refresh Token in Redis (prevent using revoked tokens)
        if (!validateRefreshToken(userId, token)) {
            throw TokenException.expired();
        }
        
        // 4. Delete all old tokens before generating new ones
        // This ensures proper token rotation and forces single sign-on
        delete(userId);
        
        // 5. Generate and return new tokens
        Map<String, String> tokens = get(userId);
        return new RefreshResponse(tokens.get("accessToken"), tokens.get("refreshToken"));
    }
    
    private boolean validateAccessToken(String userId, String token) {
        // 1. Validate JWT format and signature
        if (!jwtUtils.validateAccessToken(token)) {
            return false;
        }
        
        // 2. Retrieve the stored token from Redis
        String storedToken = getAccessToken(userId);
        
        // 3. Verify that the provided token matches the one stored in Redis
        return storedToken != null && storedToken.equals(token);
    }
    
    private boolean validateRefreshToken(String userId, String refreshToken) {
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
        try {
            // 1. Extract token from request
            String token = extractTokenFromRequest(request);
            
            // 2. Get user ID from token (this validates JWT format and signature)
            String userId = jwtUtils.getUserIdFromToken(token);
            
            // 3. Validate token in Redis (prevent using revoked tokens)
            if (!validateAccessToken(userId, token)) {
                throw TokenException.expired();
            }
            
            return Long.valueOf(userId);
        } catch (Exception e) {
            // Catch JWT parsing errors and convert to TokenException
            throw TokenException.invalid();
        }
    }
}