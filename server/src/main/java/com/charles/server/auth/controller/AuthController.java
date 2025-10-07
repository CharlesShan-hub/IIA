package com.charles.server.auth.controller;

import java.util.HashMap;
import java.util.Map;

import com.charles.server.auth.dto.*;
import com.charles.server.auth.dto.*;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.AuthService;
import com.charles.server.auth.service.TokenService;
import com.charles.server.utils.JwtUtils;
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
    private final JwtUtils jwtUtils;
    private final TokenService tokenService;
    
    // 登录
    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody @Valid LoginRequest dto) {
        try {
            LoginResponse response = authService.login(dto);
            log.info("用户请求登录成功, 邮箱: {}", dto.getEmail());
            log.debug("Token: {}", response.getToken());
            log.debug("RefreshToken: {}", response.getRefreshToken());
            return ResponseUtils.buildSuccessResponse(response, "success");
        } catch (Exception e) {
            log.info("用户登录失败, 邮箱: {}, 错误信息: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 获取用户信息
    @GetMapping("/profile")
    public Map<String, Object> profile(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            ProfileResponse response = authService.profile(userId.toString());
            log.info("用户信息请求, ID: {}", userId);
            return ResponseUtils.buildSuccessResponse(response, "success");
        } catch (Exception e) {
            log.info("用户信息请求失败, token: {}, 错误信息: {}", tokenService.extractTokenFromRequest(request), e.getMessage(), e);
            return ResponseUtils.buildUnauthorizedResponse("认证失败：" + e.getMessage());
        }
    }

    // 登出
    @PostMapping("/logout")
    public Map<String, Object> logout(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("用户登出请求, 用户ID: {}", userId);
            tokenService.deleteAllTokens(userId.toString());
            log.info("用户登出成功, 用户ID: {}", userId);
            return ResponseUtils.buildEmptySuccessResponse("登出成功");
        } catch (Exception e) {
            log.error("用户登出失败，错误信息: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 发送验证码
    @PostMapping("/send-code")
    public Map<String, Object> sendCode(@RequestBody @Valid SendCodeRequest dto) {
        try {
            authService.sendCode(dto.getEmail());
            log.info("验证码已成功发送至邮箱: {}", dto.getEmail());
            return ResponseUtils.buildSuccessResponse(null);
        } catch (Exception e) {
            log.error("发送验证码失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 注册接口
    @PostMapping("/register")
    public Map<String, Object> register(@RequestBody @Valid RegisterRequest dto) {
        log.info("用户注册请求，邮箱: {}", dto.getEmail());
        try {
            RegisterResponse response = authService.register(dto);
            log.info("用户注册成功，邮箱: {}，用户ID: {}", dto.getEmail(), response.getUserId());
            return ResponseUtils.buildSuccessResponse(response, "注册成功");
        } catch (Exception e) {
            log.error("用户注册失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 刷新AccessToken
    @PostMapping("/refresh")
    public Map<String, Object> refreshToken(@RequestBody Map<String, String> request) {
        String refreshToken = request.get("refreshToken");
        log.info("刷新AccessToken请求");
        
        try {
            // 验证Refresh Token
            if (refreshToken == null || !jwtUtils.validateRefreshToken(refreshToken)) {
                throw new RuntimeException("无效的Refresh Token");
            }
            
            // 获取用户ID
            String userId = jwtUtils.getUserIdFromToken(refreshToken);
            
            // 验证Redis中的Refresh Token
            if (!tokenService.validateRefreshToken(userId, refreshToken)) {
                throw new RuntimeException("Refresh Token已过期");
            }
            
            // 生成新的AccessToken
            String newAccessToken = jwtUtils.generateAccessToken(userId);
            
            // 存储新的AccessToken到Redis
            tokenService.storeAccessToken(userId, newAccessToken);
            
            // 设置响应数据
            Map<String, Object> data = new HashMap<>();
            data.put("token", newAccessToken);
            
            log.info("刷新AccessToken成功，用户ID: {}", userId);
            return ResponseUtils.buildSuccessResponse(data, "刷新令牌成功");
        } catch (Exception e) {
            log.error("刷新AccessToken失败，错误信息: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    /**
     * 重置密码接口
     * @param resetData 包含邮箱、验证码和新密码的请求数据
     * @return 重置结果
     */
    @PostMapping("/reset-password")
    public Map<String, Object> resetPassword(@RequestBody Map<String, String> resetData) {
        String email = resetData.get("email");
        String code = resetData.get("code");
        String newPassword = resetData.get("newPassword");
        
        log.info("用户重置密码请求，邮箱: {}", email);
        try {
            // 1. 验证邮箱格式
            if (email == null || !email.matches("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")) {
                throw new RuntimeException("邮箱格式不正确");
            }
            
            // 2. 验证验证码
            authService.verifyCode(email, code);
            
            // 3. 验证新密码
            if (newPassword == null || newPassword.length() < 6 || newPassword.length() > 20) {
                throw new RuntimeException("密码长度需6-20位");
            }
            
            // 4. 执行密码重置
            authService.resetPassword(email, newPassword);
            log.info("用户密码重置成功，邮箱: {}", email);
            
            // 使用 ResponseUtils 构建成功响应
            Map<String, Object> data = new HashMap<>();
            data.put("success", true);
            return ResponseUtils.buildSuccessResponse(data, "密码重置成功");
        } catch (Exception e) {
            log.error("用户密码重置失败，邮箱: {}，错误信息: {}", email, e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}
