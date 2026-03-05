package com.charles.server.auth.service.impl;

import com.charles.server.auth.exception.UserNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.charles.server.auth.dto.*;
import com.charles.server.auth.entity.*;
import com.charles.server.auth.mapper.*;
import com.charles.server.auth.service.*;
import com.charles.server.auth.exception.*;
import com.charles.server.utils.JwtUtils;
import com.charles.server.auth.mapper.ProfileMapper;

import org.springframework.transaction.annotation.Transactional;
import lombok.extern.slf4j.Slf4j;
import lombok.RequiredArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Data;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final UserMapper userMapper;
    private final ProfileMapper profileMapper;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtils jwtUtils;
    private final TokenService tokenService;
    private final MailService mailService;

    @Data
    @AllArgsConstructor
    private static class TokenPair {
        private String accessToken;
        private String refreshToken;
    }

    private TokenPair generateAndStoreTokens(String userId) {
        // Generate Tokens
        String accessToken = jwtUtils.generateAccessToken(userId);
        String refreshToken = jwtUtils.generateRefreshToken(userId);
        
        // Store Tokens to Redis
        tokenService.storeAccessToken(userId, accessToken);
        tokenService.storeRefreshToken(userId, refreshToken);

        return new TokenPair(accessToken, refreshToken);
    }

    private String generateDefaultUsername(String providedUsername, String email) {
        // If provided username is not empty, use it; otherwise, use email prefix
        if (providedUsername != null && !providedUsername.trim().isEmpty()) {
            return providedUsername.trim();
        }
        return email.split("@")[0];
    }

    @Override
    public LoginResponse login(LoginRequest dto) {
        // 1. Check all user profile
        UserAll userAll = userMapper.findAllByEmail(dto.getEmail());
        if (userAll == null) {
            throw new UserNotFoundException(dto.getEmail());
        }

        // 2. Check password
        if (!passwordEncoder.matches(dto.getPassword(), userAll.getPasswordHash())) {
            throw new InvalidCredentialsException();
        }

        // 3. Generate and store tokens
        String userId = userAll.getUserId().toString();
        TokenPair tokenPair = generateAndStoreTokens(userId);

        // 4. Return LoginResponse
        LoginResponse response = new LoginResponse();
        response.setToken(tokenPair.getAccessToken());
        response.setRefreshToken(tokenPair.getRefreshToken());
        response.setUserId(userId);
        return response;
    }

    @Override
    public ProfileResponse profile(String userId) {
        Profile profile = profileMapper.findById(Long.valueOf(userId));
        if (profile == null) {
            throw new UserNotFoundException(userId);
        }

        ProfileResponse response = new ProfileResponse();
        response.setUserName(profile.getUsername());
        response.setUserId(profile.getUserId());
        return response;
    }

    @Override
    @Transactional
    public RegisterResponse register(RegisterRequest dto) {
        // 1. Check if email already exists
        if (userMapper.existsByEmail(dto.getEmail())) {
            throw new EmailAlreadyRegisteredException(dto.getEmail());
        }
        
        // 2. Create Account (password hash)
        Account account = new Account();
        account.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        userMapper.insertAccount(account); // after insert, userId will be auto-set
        
        // 3. Create Profile
        Profile profile = new Profile();
        profile.setUserId(account.getUserId());
        String username = generateDefaultUsername(dto.getUsername(), dto.getEmail());
        profile.setUsername(username);
        userMapper.insertProfile(profile);
        
        // 4. Create Mail record
        Mail mail = new Mail();
        mail.setEmail(dto.getEmail());
        mail.setUserId(account.getUserId());
        userMapper.insertMail(mail);
        
        // 5. Generate and store tokens
        TokenPair tokenPair = generateAndStoreTokens(account.getUserId().toString());
        
        // 6. Build response
        RegisterResponse response = new RegisterResponse();
        response.setUserId(account.getUserId());
        response.setToken(tokenPair.getAccessToken());
        response.setRefreshToken(tokenPair.getRefreshToken());
        return response;
    }

    @Override
    @Transactional
    public void resetPassword(ResetPasswordRequest dto) {
        // 1. Verify Code
        mailService.verifyCode(dto.getEmail(), dto.getCode());
        
        // 2. Check all user profile
        UserAll userDetails = userMapper.findAllByEmail(dto.getEmail());
        if (userDetails == null) {
            throw new UserNotFoundException(dto.getEmail());
        }
        
        // 3. Update password
        Account account = new Account();
        account.setUserId(userDetails.getUserId());
        account.setPasswordHash(passwordEncoder.encode(dto.getNewPassword()));
        userMapper.updateAccount(account);
    }

    @Override
    public RefreshResponse refreshAccessToken(String refreshToken) {
        // Validate Refresh Token
        if (refreshToken == null || !jwtUtils.validateRefreshToken(refreshToken)) {
            throw TokenException.invalid();
        }
        
        // Get user ID
        String userId = jwtUtils.getUserIdFromToken(refreshToken);
        
        // Validate Refresh Token in Redis
        if (!tokenService.validateRefreshToken(userId, refreshToken)) {
            throw TokenException.expired();
        }
        
        // Generate new Access Token
        String newAccessToken = jwtUtils.generateAccessToken(userId);
        
        // Store new Access Token in Redis
        tokenService.storeAccessToken(userId, newAccessToken);

        // Return DTO instead of building response
        return new RefreshResponse(newAccessToken);
    }
}