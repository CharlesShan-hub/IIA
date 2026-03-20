package com.charles.server.auth.service;

import com.charles.server.auth.dto.*;

public interface AuthService {
    /**
     * Login via email and password
     * @param dto login request dto
     * @return login response dto
     */
    LoginVO login(LoginDTO dto);

    /**
     * Register via email and password
     * @param dto register request dto
     * @return register response dto
     */
    RegisterVO register(RegisterDTO dto);

    /**
     * Get user profile
     */
    ProfileVO profile(String userId);
    
    /**
     * Reset user password
     */
    void resetPassword(ResetPasswordDTO dto);
}