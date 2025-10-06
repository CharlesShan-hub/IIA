package com.charles.server.iia.auth.service;

import com.charles.server.iia.auth.dto.*;

public interface AuthService {
    LoginResponse login(LoginRequest dto);
    RegisterResponse register(RegisterRequest dto);
    ProfileResponse profile(String userId);
    void sendCode(String email);
    void verifyCode(String email, String inputCode);
    void resetPassword(String email, String newPassword);
}
