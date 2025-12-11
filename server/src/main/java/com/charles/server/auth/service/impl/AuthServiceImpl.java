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

import jakarta.transaction.Transactional;
import lombok.extern.slf4j.Slf4j;
import lombok.RequiredArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Data;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final AccountMapper accountMapper;
    private final ProfileMapper profileMapper;
    private final MailMapper mailMapper;
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
        // 1. Get authId by email
        Mail mail = mailMapper.findByEmail(dto.getEmail());
        if (mail == null) {
            throw new UserNotFoundException(dto.getEmail());
        }

        // 2. Get Account record by authId
        Account account = accountMapper.findById(mail.getUserId());
        if (!passwordEncoder.matches(dto.getPassword(), account.getPasswordHash())) {
            throw new InvalidCredentialsException();
        }

        // 3. Generate and store Tokens
        String userId = account.getUserId().toString();
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
        Account account = accountMapper.findById(Long.valueOf(userId));
        if (account == null) {
            throw new UserNotFoundException(userId);
        }
        Mail mail = mailMapper.findByAuthId(Long.valueOf(userId));
        Profile profile = profileMapper.findById(Long.valueOf(userId));

        ProfileResponse response = new ProfileResponse();
        response.setEmail(mail.getEmail());
        response.setUserName(profile.getUsername());
        response.setUserId(account.getUserId());
        return response;
    }

    @Override
    @Transactional
    public RegisterResponse register(RegisterRequest dto) {
        // 1. Verify Code
        mailService.verifyCode(dto.getEmail(), dto.getCode());

        // 2. Check if email is already registered
        if (mailMapper.existsByEmail(dto.getEmail())) {
            throw new EmailAlreadyRegisteredException(dto.getEmail());
        }

        // 3. Register Process: Create Account first 
        Account account = new Account();
        account.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        accountMapper.insert(account); // after insert, userId will be auto-set

        // 4. Register Process: Create User Profile
        Profile profile = new Profile();
        profile.setUserId(account.getUserId()); // use the new account's userId
        String username = generateDefaultUsername(dto.getUsername(), dto.getEmail());
        profile.setUsername(username);
        profileMapper.insert(profile);

        // 5. Register Process: Create Mail Record
        Mail mail = new Mail();
        mail.setEmail(dto.getEmail());
        mail.setUserId(account.getUserId());
        mailMapper.insert(mail);

        // 6. Generate and store AccessToken
        TokenPair tokenPair = generateAndStoreTokens(account.getUserId().toString());

        // 7. Build RegisterResponse
        RegisterResponse response = new RegisterResponse();
        response.setUserId(account.getUserId());
        response.setPasswordHash(account.getPasswordHash());
        response.setToken(tokenPair.getAccessToken());
        response.setRefreshToken(tokenPair.getRefreshToken());

        return response;
    }

    @Override
    @Transactional
    public void resetPassword(ResetPasswordRequest dto) {
        // 1. Verify Code
        mailService.verifyCode(dto.getEmail(), dto.getCode());

        // 2. Find Mail record by email
        Mail mail = mailMapper.findByEmail(dto.getEmail());
        if (mail == null) {
            throw new UserNotFoundException(dto.getEmail());
        }

        // 3. Find Account record by authId
        Account account = accountMapper.findById(mail.getUserId());
        if (account == null) {
            throw new UserNotFoundException(mail.getUserId().toString());
        }

        // 4. Update password (using BCrypt encryption)
        account.setPasswordHash(passwordEncoder.encode(dto.getNewPassword()));
        accountMapper.updateById(account);
    }

    @Override
    public RefreshResponse refreshAccessToken(String refreshToken) {
        log.info("Refreshing access token");
        
        // Validate Refresh Token
        if (refreshToken == null || !jwtUtils.validateRefreshToken(refreshToken)) {
            throw new InvalidTokenException();
        }
        
        // Get user ID
        String userId = jwtUtils.getUserIdFromToken(refreshToken);
        
        // Validate Refresh Token in Redis
        if (!tokenService.validateRefreshToken(userId, refreshToken)) {
            throw new ExpiredTokenException();
        }
        
        // Generate new Access Token
        String newAccessToken = jwtUtils.generateAccessToken(userId);
        
        // Store new Access Token in Redis
        tokenService.storeAccessToken(userId, newAccessToken);
        
        log.info("Refreshed Access Token successfully, user ID: {}", userId);
        
        // Return DTO instead of building response
        return new RefreshResponse(newAccessToken);
    }
}