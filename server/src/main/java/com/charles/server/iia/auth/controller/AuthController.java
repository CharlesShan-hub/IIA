package com.charles.server.iia.auth.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.iia.auth.dto.LoginDTO;
import com.charles.server.iia.auth.dto.RegisterDTO;
import com.charles.server.iia.auth.dto.SendCodeDTO;
import com.charles.server.iia.auth.entity.AuthAccount;
import com.charles.server.iia.auth.service.AuthService;
import com.charles.server.iia.auth.service.TokenService;
import com.charles.server.iia.auth.utils.JwtUtils;

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

    // 1. 原有登录接口（已添加日志）
    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> login(@RequestBody @Valid LoginDTO dto) {
        log.info("用户登录请求，邮箱: {}", dto.getEmail());
        try {
            // 执行登录验证
            AuthAccount account = authService.login(dto);
            log.info("用户登录成功，邮箱: {}", dto.getEmail());
            
            // 使用JWT工具类生成Token
            String token = jwtUtils.generateJwtToken(account.getId().toString());
            
            // 存储Token到Redis
            tokenService.storeToken(account.getId().toString(), token);
            
            // 获取用户完整信息
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("id", account.getId());
            userInfo.put("authId", account.getId());
            // 可以在这里添加更多用户信息
            
            // 设置响应数据
            Map<String, Object> response = new HashMap<>();
            response.put("token", token);
            response.put("user", userInfo);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("用户登录失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 用户登出接口
     * @param userId 用户ID
     * @return 登出结果
     */
    @PostMapping("/logout/{userId}")
    public ResponseEntity<Map<String, Object>> logout(@PathVariable Long userId) {
        log.info("用户登出请求，用户ID: {}", userId);
        try {
            // 从Redis删除Token使其失效
            tokenService.deleteToken(userId.toString());
            
            // 构造响应数据
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "登出成功");
            
            log.info("用户登出成功，用户ID: {}", userId);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("用户登出失败，用户ID: {}，错误信息: {}", userId, e.getMessage(), e);
            throw e;
        }
    }

    // 2. 改造后的注册接口（新增验证码校验）（已添加日志）
    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> register(@RequestBody @Valid RegisterDTO dto) {
        log.info("用户注册请求，邮箱: {}", dto.getEmail());
        try {
            // 执行注册操作（包含验证码校验）
            AuthAccount account = authService.register(dto);
            log.info("用户注册成功，邮箱: {}，用户ID: {}", dto.getEmail(), account.getId());
            
            // 使用JWT工具类生成Token
            String token = jwtUtils.generateJwtToken(account.getId().toString());
            
            // 存储Token到Redis
            tokenService.storeToken(account.getId().toString(), token);
            
            // 获取用户完整信息
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("id", account.getId());
            userInfo.put("authId", account.getId());
            // 可以在这里添加更多用户信息
            
            // 设置响应数据
            Map<String, Object> response = new HashMap<>();
            response.put("token", token);
            response.put("user", userInfo);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("用户注册失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            throw e;
        }
    }

    // 3. 新增验证码发送接口
    @PostMapping("/send-code")
    public ResponseEntity<Void> sendCode(@RequestBody @Valid SendCodeDTO dto) {
        log.info("开始发送验证码请求，目标邮箱: {}", dto.getEmail());
        try {
            authService.sendCode(dto.getEmail());
            log.info("验证码已成功发送至邮箱: {}", dto.getEmail());
        } catch (Exception e) {
            log.error("发送验证码失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            throw e;
        }
        return ResponseEntity.ok().build();
    }

    /**
     * 重置密码接口
     * @param resetData 包含邮箱、验证码和新密码的请求数据
     * @return 重置结果
     */
    @PostMapping("/reset-password")
    public ResponseEntity<Map<String, Object>> resetPassword(@RequestBody Map<String, String> resetData) {
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
            if (!authService.verifyCode(email, code)) {
                throw new RuntimeException("验证码验证失败");
            }
            
            // 3. 验证新密码
            if (newPassword == null || newPassword.length() < 6 || newPassword.length() > 20) {
                throw new RuntimeException("密码长度需6-20位");
            }
            
            // 4. 执行密码重置
            authService.resetPassword(email, newPassword);
            log.info("用户密码重置成功，邮箱: {}", email);
            
            // 构造响应数据
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "密码重置成功");
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("用户密码重置失败，邮箱: {}，错误信息: {}", email, e.getMessage(), e);
            throw e;
        }
    }
}
