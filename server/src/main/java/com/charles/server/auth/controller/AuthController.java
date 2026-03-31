package com.charles.server.auth.controller;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import com.charles.server.auth.dto.*;
import com.charles.server.auth.service.*;
import com.charles.server.utils.ResponseUtils;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;

@Slf4j
@RestController
@RequestMapping("/api/auth")
@CrossOrigin
@RequiredArgsConstructor
@Tag(name = "Authentication Management", description = "User authentication, registration, password reset APIs")
public class AuthController {
    private final AuthService authService;
    private final TokenService tokenService;
    private final MailService mailService;
    
    @PostMapping("/login")
    @Operation(
        summary = "User Login",
        description = "Login to the system using email and password, returns access token and refresh token"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Login successful"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication failed, invalid email or password")
    })
    public ResponseUtils<LoginVO> login(@RequestBody @Valid LoginDTO dto) {
        LoginVO response = authService.login(dto);
        log.info("User login succeeded, email: {}", dto.getEmail());
        return ResponseUtils.buildSuccessResponse(response, "login succeeded");
    }

    @GetMapping("/profile")
    @Operation(
        summary = "Get User Profile",
        description = "Get detailed information of the currently logged-in user, requires Bearer Token authentication"
    )
    @SecurityRequirement(name = "bearer-jwt")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Successfully retrieved"),
        @ApiResponse(responseCode = "401", description = "Unauthorized or invalid token")
    })
    public ResponseUtils<ProfileVO> profile(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        ProfileVO response = authService.profile(userId.toString());
        log.info("User profile request, ID: {}", userId);
        return ResponseUtils.buildSuccessResponse(response, "user profile");
    }

    @PostMapping("/logout")
    @Operation(
        summary = "User Logout",
        description = "Logout current user, invalidate token"
    )
    @SecurityRequirement(name = "bearer-jwt")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Logout successful"),
        @ApiResponse(responseCode = "401", description = "Unauthorized or invalid token")
    })
    public ResponseUtils<Void> logout(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        tokenService.delete(userId.toString());
        log.info("User logout succeeded, user ID: {}", userId);
        return ResponseUtils.buildEmptySuccessResponse("logout succeeded");
    }

    @PostMapping("/register")
    @Operation(
        summary = "User Registration",
        description = "Register a new user account"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Registration successful"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters or email already exists")
    })
    public ResponseUtils<RegisterVO> register(@RequestBody @Valid RegisterDTO dto) {
        RegisterVO response = authService.register(dto);
        log.info("User registration succeeded, email: {}, user ID: {}", dto.getEmail(), response.getUserId());
        return ResponseUtils.buildSuccessResponse(response, "registration succeeded");
    }

    @PostMapping("/reset-password")
    @Operation(
        summary = "Reset Password",
        description = "Reset user password using verification code"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Password reset successful"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters or verification code"),
        @ApiResponse(responseCode = "404", description = "User not found")
    })
    public ResponseUtils<Void> resetPassword(@RequestBody @Valid ResetPasswordDTO dto) {
        authService.resetPassword(dto);
        log.info("Password reset succeeded, email: {}", dto.getEmail());
        return ResponseUtils.buildEmptySuccessResponse("password reset succeeded");
    }

    @PostMapping("/refresh")
    @Operation(
        summary = "Refresh Access Token",
        description = "Get new access token using refresh token"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Token refresh successful"),
        @ApiResponse(responseCode = "401", description = "Refresh token is invalid or expired")
    })
    public ResponseUtils<RefreshVO> refreshToken(@RequestBody @Valid RefreshDTO dto) {
        RefreshVO response = tokenService.refresh(dto.getRefreshToken());
        log.info("Refreshed Access Token successfully");
        return ResponseUtils.buildSuccessResponse(response, "refresh token succeeded");
    }

    @PostMapping("/send-code")
    @Operation(
        summary = "Send Verification Code",
        description = "Send a verification code to the user's email address for password reset. " +
                     "In development environment, the code is returned in the response for testing."
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Verification code sent successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid email address"),
        @ApiResponse(responseCode = "404", description = "User not found")
    })
    public ResponseUtils<SendCodeVO> sendCode(@RequestBody @Valid SendCodeDTO dto) {
        SendCodeVO response = mailService.sendVerificationCode(dto.getEmail());
        log.info("Verification code sent to email: {}", dto.getEmail());
        return ResponseUtils.buildSuccessResponse(response, "Verification code sent");
    }
}