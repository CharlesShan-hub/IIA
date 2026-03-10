package com.charles.server.auth.controller;

import java.util.Map;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import com.charles.server.auth.dto.*;
import com.charles.server.auth.service.*;
import com.charles.server.utils.ResponseUtils;

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
        LoginResponse response = authService.login(dto);
        log.info("User login succeeded, email: {}", dto.getEmail());
        return ResponseUtils.buildSuccessResponse(response, "login succeeded");
    }

    // Get user profile
    @GetMapping("/profile")
    public Map<String, Object> profile(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        ProfileResponse response = authService.profile(userId.toString());
        log.info("User profile request, ID: {}", userId);
        return ResponseUtils.buildSuccessResponse(response, "user profile");
    }

    // Logout
    @PostMapping("/logout")
    public Map<String, Object> logout(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        tokenService.delete(userId.toString());
        log.info("User logout succeeded, user ID: {}", userId);
        return ResponseUtils.buildEmptySuccessResponse("logout succeeded");
    }

    // Register API
    @PostMapping("/register")
    public Map<String, Object> register(@RequestBody @Valid RegisterRequest dto) {
        RegisterResponse response = authService.register(dto);
        log.info("User registration succeeded, email: {}, user ID: {}", dto.getEmail(), response.getUserId());
        return ResponseUtils.buildSuccessResponse(response, "registration succeeded");
    }

    // Reset Password
    @PostMapping("/reset-password")
    public Map<String, Object> resetPassword(@RequestBody @Valid ResetPasswordRequest dto) {
        authService.resetPassword(dto);
        log.info("Password reset succeeded, email: {}", dto.getEmail());
        return ResponseUtils.buildEmptySuccessResponse("password reset succeeded");
    }

    // Refresh Access Token
    @PostMapping("/refresh")
    public Map<String, Object> refreshToken(@RequestBody @Valid RefreshTokenRequest dto) {
        RefreshResponse response = tokenService.refresh(dto.getRefreshToken());
        log.info("Refreshed Access Token successfully");
        return ResponseUtils.buildSuccessResponse(response, "refresh token succeeded");
    }

    // Send verification code
    @PostMapping("/send-code")
    public Map<String, Object> sendCode(@RequestBody @Valid SendCodeRequest dto) {
        mailService.sendVerificationCode(dto.getEmail());
        log.info("Verification code sent to email: {}", dto.getEmail());
        return ResponseUtils.buildEmptySuccessResponse("Verification code sent");
    }
}