package com.charles.server.auth.service.impl;

import java.util.Map;
import java.util.concurrent.TimeUnit;

import com.charles.server.auth.dto.RefreshVO;
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

    @Value("${spring.redis.key-prefix:iia:}")
    private String redisKeyPrefix;

    private String withPrefix(String key) {
        String safeKey = Objects.requireNonNull(key, "key must not be null");
        if (!StringUtils.hasText(redisKeyPrefix)) {
            return safeKey;
        }
        if (redisKeyPrefix.endsWith(":")) {
            return redisKeyPrefix + safeKey;
        }
        return redisKeyPrefix + ":" + safeKey;
    }

    private void storeAccessToken(String userId, String token) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");
        String safeToken = Objects.requireNonNull(token, "token must not be null");
        String key = Objects.requireNonNull(withPrefix("token:access:user:" + safeUserId), "redis key must not be null");
        redisTemplate.opsForValue().set(key, safeToken, tokenExpiration, TimeUnit.HOURS);
        
        // Add reverse mapping: accessToken -> userId
        String reverseKey = Objects.requireNonNull(withPrefix("token:access:reverse:" + safeToken), "redis key must not be null");
        redisTemplate.opsForValue().set(reverseKey, safeUserId, tokenExpiration, TimeUnit.HOURS);
    }
    
    private void storeRefreshToken(String userId, String refreshToken) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");
        String safeRefreshToken = Objects.requireNonNull(refreshToken, "refreshToken must not be null");
        String key = Objects.requireNonNull(withPrefix("token:refresh:user:" + safeUserId), "redis key must not be null");
        redisTemplate.opsForValue().set(key, safeRefreshToken, refreshTokenExpiration, TimeUnit.HOURS);
        
        // Add reverse mapping: refreshToken -> userId
        String reverseKey = Objects.requireNonNull(withPrefix("token:refresh:reverse:" + safeRefreshToken), "redis key must not be null");
        redisTemplate.opsForValue().set(reverseKey, safeUserId, refreshTokenExpiration, TimeUnit.HOURS);
    }
    
    private String getAccessToken(String userId) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");
        String key = Objects.requireNonNull(withPrefix("token:access:user:" + safeUserId), "redis key must not be null");
        return redisTemplate.opsForValue().get(key);
    }
    
    private String getRefreshToken(String userId) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");
        String key = Objects.requireNonNull(withPrefix("token:refresh:user:" + safeUserId), "redis key must not be null");
        return redisTemplate.opsForValue().get(key);
    }

    @Override
    public Map<String, String> get(String userId) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");

        // Generate Tokens
        String accessToken = Objects.requireNonNull(jwtUtils.generateAccessToken(safeUserId), "accessToken must not be null");
        String refreshToken = Objects.requireNonNull(jwtUtils.generateRefreshToken(safeUserId), "refreshToken must not be null");

        // Store Tokens to Redis
        storeAccessToken(safeUserId, accessToken);
        storeRefreshToken(safeUserId, refreshToken);

        return Map.of("accessToken", accessToken, "refreshToken", refreshToken);
    }

    private void deleteAccessToken(String userId) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");
        String key = Objects.requireNonNull(withPrefix("token:access:user:" + safeUserId), "redis key must not be null");
        String token = redisTemplate.opsForValue().get(key);
        redisTemplate.delete(key);
        if (token != null) {
            // if the token exists, delete the reverse mapping
            String reverseKey = Objects.requireNonNull(withPrefix("token:access:reverse:" + token), "redis key must not be null");
            redisTemplate.delete(reverseKey);
        }
    }

    private void deleteRefreshToken(String userId) {
        String safeUserId = Objects.requireNonNull(userId, "userId must not be null");
        String key = Objects.requireNonNull(withPrefix("token:refresh:user:" + safeUserId), "redis key must not be null");
        String token = redisTemplate.opsForValue().get(key);
        redisTemplate.delete(key);
        if (token != null) {
            // if the token exists, delete the reverse mapping
            String reverseKey = Objects.requireNonNull(withPrefix("token:refresh:reverse:" + token), "redis key must not be null");
            redisTemplate.delete(reverseKey);
        }
    }

    public void delete(String userId) {
        deleteAccessToken(userId);
        deleteRefreshToken(userId);
    }

    @Override
    public RefreshVO refresh(String token) {
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
        return new RefreshVO(tokens.get("accessToken"), tokens.get("refreshToken"));
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