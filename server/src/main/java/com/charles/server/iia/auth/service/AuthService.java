package com.charles.server.iia.auth.service;

import java.util.Map;

import com.charles.server.iia.auth.dto.LoginDTO;
import com.charles.server.iia.auth.dto.RegisterDTO;
import com.charles.server.iia.auth.entity.AuthAccount;

public interface AuthService {
    Map<String, Object> login(LoginDTO dto);
    Map<String, Object> getUserInfo(String userId);
    AuthAccount register(RegisterDTO dto);
    void sendCode(String email);
    boolean verifyCode(String email, String inputCode);
    void resetPassword(String email, String newPassword);
    boolean validateToken(String token);
    String getUserIdFromToken(String token);
}
