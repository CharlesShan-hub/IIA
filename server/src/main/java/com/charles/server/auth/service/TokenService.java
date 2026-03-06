package com.charles.server.auth.service;

import jakarta.servlet.http.HttpServletRequest;

import java.util.Map;
import com.charles.server.auth.dto.RefreshResponse;

public interface TokenService {

    /**
     * Refresh tokens using refresh token
     * @param token JWT Refresh Token
     * @return New tokens
     */
    RefreshResponse refresh(String token);

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
     * @param request HttpServletRequest object
     * @return userId
     * @throws RuntimeException
     */
    Long getUserIdFromRequest(HttpServletRequest request);
}