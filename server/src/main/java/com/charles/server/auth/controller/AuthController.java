package com.charles.server.auth.controller;

import java.util.Map;

import com.charles.server.auth.dto.*;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.*;
import com.charles.server.utils.ResponseUtils;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/auth")
@CrossOrigin
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;
    private final TokenService tokenService;
    private final MailService mailService;
    
    // Login
    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody @Valid LoginRequest dto) {
        try {
            LoginResponse response = authService.login(dto);
            log.info("User login succeeded, email: {}", dto.getEmail());
            return ResponseUtils.buildSuccessResponse(response, "login succeeded");
        } catch (Exception e) {
            log.info("User login failed, email: {}, error: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Get user profile
    @GetMapping("/profile")
    public Map<String, Object> profile(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            ProfileResponse response = authService.profile(userId.toString());
            log.info("User profile request, ID: {}", userId);
            return ResponseUtils.buildSuccessResponse(response, "user profile");
        } catch (Exception e) {
            log.info("User profile request failed, error: {}", e.getMessage(), e);
            return ResponseUtils.buildUnauthorizedResponse("Authentication failed: " + e.getMessage());
        }
    }

    // Logout
    @PostMapping("/logout")
    public Map<String, Object> logout(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User logout request, user ID: {}", userId);
            tokenService.delete(userId.toString());
            log.info("User logout succeeded, user ID: {}", userId);
            return ResponseUtils.buildEmptySuccessResponse("logout succeeded");
        } catch (Exception e) {
            log.error("User logout failed, error: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Register API
    @PostMapping("/register")
    public Map<String, Object> register(@RequestBody @Valid RegisterRequest dto) {
        log.info("User registration request, email: {}", dto.getEmail());
        try {
            RegisterResponse response = authService.register(dto);
            log.info("User registration succeeded, email: {}, user ID: {}", dto.getEmail(), response.getUserId());
            return ResponseUtils.buildSuccessResponse(response, "registration succeeded");
        } catch (Exception e) {
            log.error("User registration failed, email: {}, error: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Reset Password
    @PostMapping("/reset-password")
    public Map<String, Object> resetPassword(@RequestBody @Valid ResetPasswordRequest dto) {
        log.info("Reset password request, email: {}", dto.getEmail());
        try {
            authService.resetPassword(dto);
            log.info("Password reset succeeded, email: {}", dto.getEmail());
            return ResponseUtils.buildEmptySuccessResponse("password reset succeeded");
        } catch (Exception e) {
            log.error("Password reset failed, email: {}, error: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Refresh Access Token
    @PostMapping("/refresh")
    public Map<String, Object> refreshToken(@RequestBody @Valid RefreshTokenRequest dto) {
        log.info("Refresh Access Token request");
        try {
            Map<String, String> tokens = tokenService.refresh(dto.getRefreshToken());
            RefreshResponse response = new RefreshResponse(
                tokens.get("accessToken"), 
                tokens.get("refreshToken")
            );
            log.info("Refreshed Access Token successfully");
            return ResponseUtils.buildSuccessResponse(response, "refresh token succeeded");
        } catch (Exception e) {
            log.error("Failed to refresh Access Token, error: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Send verification code
    @PostMapping("/send-code")
    public Map<String, Object> sendCode(@RequestBody @Valid SendCodeRequest dto) {
        try {
            mailService.sendVerificationCode(dto.getEmail());
            log.info("Verification code sent to email: {}", dto.getEmail());
            return ResponseUtils.buildEmptySuccessResponse("Verification code sent");
        } catch (Exception e) {
            log.error("Failed to send verification code, email: {}, error: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}