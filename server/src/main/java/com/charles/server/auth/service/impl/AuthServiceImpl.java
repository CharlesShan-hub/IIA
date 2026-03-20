package com.charles.server.auth.service.impl;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.charles.server.auth.dto.*;
import com.charles.server.auth.entity.*;
import com.charles.server.auth.mapper.*;
import com.charles.server.auth.service.*;
import com.charles.server.auth.exception.*;
import org.springframework.transaction.annotation.Transactional;
import lombok.extern.slf4j.Slf4j;
import lombok.RequiredArgsConstructor;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final AuthMapper authMapper;
    private final ProfileMapper profileMapper;
    private final MailMapper mailMapper;
    private final PasswordEncoder passwordEncoder;
    private final TokenService tokenService;
    private final MailService mailService;

    private String generateDefaultUsername(String providedUsername, String email) {
        // If provided username is not empty, use it; otherwise, use email prefix
        if (providedUsername != null && !providedUsername.trim().isEmpty()) {
            return providedUsername.trim();
        }
        return email.split("@")[0];
    }

    @Override
    public LoginVO login(LoginDTO dto) {
        // 1. Check all user profile
        UserAll userAll = authMapper.findAllByEmail(dto.getEmail());
        if (userAll == null) {
            throw AuthException.userNotFound(dto.getEmail());
        }

        // 2. Check password
        if (!passwordEncoder.matches(dto.getPassword(), userAll.getPasswordHash())) {
            throw AuthException.invalidCredentials();
        }

        // 3. Generate and store tokens
        String userId = userAll.getUserId().toString();
        Map<String, String> tokens = tokenService.get(userId);

        // 4. Return LoginResponse
        LoginVO response = new LoginVO();
        response.setToken(tokens.get("accessToken"));
        response.setRefreshToken(tokens.get("refreshToken"));
        response.setUserId(userId);
        return response;
    }

    @Override
    public ProfileVO profile(String userId) {
        Profile profile = profileMapper.findById(Long.valueOf(userId));
        if (profile == null) {
            throw AuthException.userNotFound(userId);
        }

        ProfileVO response = new ProfileVO();
        response.setUserName(profile.getUsername());
        response.setUserId(profile.getUserId());
        return response;
    }

    @Override
    @Transactional
    public RegisterVO register(RegisterDTO dto) {
        // 1. Check if email already exists
        if (mailMapper.existsByEmail(dto.getEmail())) {
            throw AuthException.emailAlreadyRegistered(dto.getEmail());
        }
        
        // 2. Create Account (password hash)
        Account account = new Account();
        account.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        authMapper.insertAccount(account); // after insert, userId will be auto-set
        
        // 3. Create Profile
        Profile profile = new Profile();
        profile.setUserId(account.getUserId());
        String username = generateDefaultUsername(dto.getUsername(), dto.getEmail());
        profile.setUsername(username);
        profileMapper.insertProfile(profile);
        
        // 4. Create Mail record
        Mail mail = new Mail();
        mail.setEmail(dto.getEmail());
        mail.setUserId(account.getUserId());
        mailMapper.insertMail(mail);
        
        // 5. Generate and store tokens
        Map<String, String> tokens = tokenService.get(account.getUserId().toString());
        
        // 6. Build response
        RegisterVO response = new RegisterVO();
        response.setUserId(account.getUserId());
        response.setToken(tokens.get("accessToken"));
        response.setRefreshToken(tokens.get("refreshToken"));
        return response;
    }

    @Override
    @Transactional
    public void resetPassword(ResetPasswordDTO dto) {
        // 1. Verify Code
        mailService.verifyCode(dto.getEmail(), dto.getCode());
        
        // 2. Check all user profile
        UserAll userDetails = authMapper.findAllByEmail(dto.getEmail());
        if (userDetails == null) {
            throw AuthException.userNotFound(dto.getEmail());
        }
        
        // 3. Update password
        Account account = new Account();
        account.setUserId(userDetails.getUserId());
        account.setPasswordHash(passwordEncoder.encode(dto.getNewPassword()));
        authMapper.updateAccount(account);
    }
}