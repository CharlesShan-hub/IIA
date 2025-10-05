package com.charles.server.iia.auth.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
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
import com.charles.server.iia.auth.utils.TokenUtils;

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

    // 登录接口
    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody @Valid LoginDTO dto) {
        try {
            Map<String, Object> loginResult = authService.login(dto);
            log.info("用户登录成功，邮箱: {}", dto.getEmail());
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "登录成功");
            response.put("data", loginResult);
            log.info("Token: {}", loginResult.get("token"));
            log.info("RefreshToken: {}", loginResult.get("refreshToken"));
            return response;
        } catch (Exception e) {
            log.error("用户登录失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);

            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 400);
            errorResponse.put("msg", e.getMessage());
            errorResponse.put("data", null);
            return errorResponse;
        }
    }

    // 获取用户信息接口
    @GetMapping("/profile")
    public Map<String, Object> profile(HttpServletRequest request) {
        try {
            String token = TokenUtils.getTokenFromRequest(request);
            log.info("用户信息请求，Token: {}", token);
            String userId = authService.getUserIdFromToken(token);
            Map<String, Object> userInfo = authService.getUserInfo(userId);
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "success");
            response.put("data", userInfo);
            return response;
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 401);
            errorResponse.put("message", "认证失败：" + e.getMessage());
            return errorResponse;
        }
    }

    /**
     * 刷新AccessToken接口
     * @param request 刷新令牌
     * @return 新的AccessToken
     */
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
            
            // 设置响应数据 - 按照前端期望的格式包装（code, msg, data）
            Map<String, Object> data = new HashMap<>();
            data.put("token", newAccessToken);
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "刷新令牌成功");
            response.put("data", data);
            
            log.info("刷新AccessToken成功，用户ID: {}", userId);
            return response;
        } catch (Exception e) {
            log.error("刷新AccessToken失败，错误信息: {}", e.getMessage(), e);
            
            // 构造错误响应
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 400);
            errorResponse.put("msg", e.getMessage());
            errorResponse.put("data", null);
            return errorResponse;
        }
    }
    
    /**
     * 用户登出接口
     * @param userId 用户ID
     * @return 登出结果
     */
    @PostMapping("/logout/{userId}")
    public Map<String, Object> logout(@PathVariable Long userId) {
        log.info("用户登出请求，用户ID: {}", userId);
        try {
            // 从Redis删除所有Token使其失效
            tokenService.deleteAllTokens(userId.toString());
            
            // 设置响应数据 - 按照前端期望的格式包装（code, msg, data）
            Map<String, Object> data = new HashMap<>();
            data.put("success", true);
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "登出成功");
            response.put("data", data);
            
            log.info("用户登出成功，用户ID: {}", userId);
            return response;
        } catch (Exception e) {
            log.error("用户登出失败，用户ID: {}，错误信息: {}", userId, e.getMessage(), e);
            
            // 构造错误响应
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 400);
            errorResponse.put("msg", e.getMessage());
            errorResponse.put("data", null);
            return errorResponse;
        }
    }

    // 2. 改造后的注册接口（新增验证码校验）（已添加日志）
    @PostMapping("/register")
    public Map<String, Object> register(@RequestBody @Valid RegisterDTO dto) {
        log.info("用户注册请求，邮箱: {}", dto.getEmail());
        try {
            // 执行注册操作（包含验证码校验）
            AuthAccount account = authService.register(dto);
            log.info("用户注册成功，邮箱: {}，用户ID: {}", dto.getEmail(), account.getId());
            
            // 使用JWT工具类生成AccessToken
            String token = jwtUtils.generateAccessToken(account.getId().toString());
            
            // 存储AccessToken到Redis
            tokenService.storeAccessToken(account.getId().toString(), token);
            
            // 获取用户完整信息
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("id", account.getId());
            userInfo.put("authId", account.getId());
            // 可以在这里添加更多用户信息
            
            // 设置响应数据 - 按照前端期望的格式包装（code, msg, data）
            Map<String, Object> data = new HashMap<>();
            data.put("token", token);
            data.put("user", userInfo);
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "注册成功");
            response.put("data", data);
            
            return response;
        } catch (Exception e) {
            log.error("用户注册失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            
            // 构造错误响应
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 400);
            errorResponse.put("msg", e.getMessage());
            errorResponse.put("data", null);
            return errorResponse;
        }
    }

    // 3. 新增验证码发送接口
    @PostMapping("/send-code")
    public Map<String, Object> sendCode(@RequestBody @Valid SendCodeDTO dto) {
        log.info("开始发送验证码请求，目标邮箱: {}", dto.getEmail());
        try {
            authService.sendCode(dto.getEmail());
            log.info("验证码已成功发送至邮箱: {}", dto.getEmail());
            
            // 设置响应数据 - 按照前端期望的格式包装（code, msg, data）
            Map<String, Object> data = new HashMap<>();
            data.put("success", true);
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "验证码发送成功");
            response.put("data", data);
            
            return response;
        } catch (Exception e) {
            log.error("发送验证码失败，邮箱: {}，错误信息: {}", dto.getEmail(), e.getMessage(), e);
            
            // 构造错误响应
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 400);
            errorResponse.put("msg", e.getMessage());
            errorResponse.put("data", null);
            return errorResponse;
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
            
            // 构造响应数据 - 按照前端期望的格式包装（code, msg, data）
            Map<String, Object> data = new HashMap<>();
            data.put("success", true);
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "密码重置成功");
            response.put("data", data);
            
            return response;
        } catch (Exception e) {
            log.error("用户密码重置失败，邮箱: {}，错误信息: {}", email, e.getMessage(), e);
            
            // 构造错误响应
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 400);
            errorResponse.put("msg", e.getMessage());
            errorResponse.put("data", null);
            return errorResponse;
        }
    }
}
