package com.charles.server.auth.service;

import com.charles.server.auth.dto.*;

public interface AuthService {
    /**
     * Login via email and password
     * @param dto login request dto
     * @return login response dto
     */
    LoginResponse login(LoginRequest dto);

    /**
     * Register via email and password
     * @param dto register request dto
     * @return register response dto
     */
    RegisterResponse register(RegisterRequest dto);

    /**
     * Get user profile
     */
    ProfileResponse profile(String userId);
    
    /**
     * Reset user password
     */
    void resetPassword(String email, String newPassword);
    
    /**
     * Refresh access token using refresh token
     * @param refreshToken the refresh token
     * @return RefreshResponse containing new access token
     */
    RefreshResponse refreshAccessToken(String refreshToken);
}