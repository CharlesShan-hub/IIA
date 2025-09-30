package com.charles.server.iia.auth.service;

import com.charles.server.iia.auth.dto.LoginDTO;
import com.charles.server.iia.auth.dto.RegisterDTO;
import com.charles.server.iia.auth.entity.AuthAccount;

public interface AuthService {
    AuthAccount login(LoginDTO dto);
    AuthAccount register(RegisterDTO dto);
    void sendCode(String email);
    boolean verifyCode(String email, String inputCode);
    void resetPassword(String email, String newPassword);
}
