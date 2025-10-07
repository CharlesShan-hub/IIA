package com.charles.server.auth.service.impl;

import java.util.Random;
import java.util.concurrent.TimeUnit;

import com.charles.server.auth.dto.*;
import com.charles.server.iia.auth.dto.*;
import com.charles.server.auth.entity.Account;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.charles.server.auth.entity.Mail;
import com.charles.server.auth.entity.Profile;
import com.charles.server.auth.mapper.AccountMapper;
import com.charles.server.auth.mapper.MailMapper;
import com.charles.server.auth.mapper.ProfileMapper;
import com.charles.server.auth.service.AuthService;
import com.charles.server.auth.service.TokenService;
import com.charles.server.utils.JwtUtils;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final AccountMapper accountMapper;
    private final ProfileMapper profileMapper;
    private final MailMapper mailMapper;
    private final PasswordEncoder passwordEncoder;
    private final JavaMailSender mailSender;
    private final StringRedisTemplate redisTemplate;
    private final JwtUtils jwtUtils;
    private final TokenService tokenService;

    @Value("${spring.mail.username}")
    private String fromEmail;

    @Override
    public LoginResponse login(LoginRequest dto) {
        // 1. 通过邮箱查找Mail记录
        Mail mail = mailMapper.findByEmail(dto.getEmail());
        if (mail == null) {
            throw new RuntimeException("邮箱不存在");
        }

        // 2. 通过authId查找AuthAccount记录
        Account account = accountMapper.findById(mail.getUserId());
        if (account == null || !passwordEncoder.matches(dto.getPassword(), account.getPasswordHash())) {
            throw new RuntimeException("密码错误");
        }

        // 3. 生成并存储Token
        String userId = account.getUserId().toString();
        String accessToken = jwtUtils.generateAccessToken(userId);
        String refreshToken = jwtUtils.generateRefreshToken(userId);

        // 存储Token到Redis
        tokenService.storeAccessToken(userId, accessToken);
        tokenService.storeRefreshToken(userId, refreshToken);

        // 直接返回Map
        LoginResponse response = new LoginResponse();
        response.setToken(accessToken);
        response.setRefreshToken(refreshToken);
        response.setUserId(userId);
        return response;
    }

    @Override
    public ProfileResponse profile(String userId) {
        Account account = accountMapper.findById(Long.valueOf(userId));
        if (account == null) {
            throw new RuntimeException("用户不存在");
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
    public void sendCode(String email) {
        // 1. 生成6位验证码
        String code = String.format("%06d", new Random().nextInt(999999));

        // 2. 缓存验证码到Redis，有效期5分钟
        String key = "email:code:" + email;
        redisTemplate.opsForValue().set(key, code, 5, TimeUnit.MINUTES);

        // 3. 发送邮件
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(fromEmail);
        message.setTo(email);
        message.setSubject("验证码");
        message.setText("您的验证码是：" + code + "，有效期5分钟。");
        mailSender.send(message);
    }

    @Override
    @Transactional
    public RegisterResponse register(RegisterRequest dto) {
        // 1. 校验验证码
        this.verifyCode(dto.getEmail(), dto.getCode());

        // 2. 检查邮箱是否已被注册
        if (mailMapper.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("邮箱已被注册");
        }

        // 3. 注册流程：先创建认证信息
        Account account = new Account();
        account.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        accountMapper.insert(account); // 插入后userId会自动设置

        // 4. 创建用户基本信息
        Profile profile = new Profile();
        profile.setUserId(account.getUserId()); // 使用刚生成的userId
        // 优先使用前端传来的用户名，如果为空则使用邮箱前缀
        String username = dto.getUsername();
        if (username == null || username.trim().isEmpty()) {
            username = dto.getEmail().split("@")[0];
        }
        profile.setUsername(username);
        profileMapper.insert(profile);

        // 5. 创建邮箱信息
        Mail mail = new Mail();
        mail.setEmail(dto.getEmail());
        mail.setUserId(account.getUserId()); // 使用刚生成的userId
        mailMapper.insert(mail);

        // 6. 构建响应
        RegisterResponse response = new RegisterResponse();
        response.setUserId(account.getUserId());
        response.setPasswordHash(account.getPasswordHash());

        // 7. 生成并存储AccessToken
        String token = jwtUtils.generateAccessToken(account.getUserId().toString());
        response.setToken(token);
        tokenService.storeAccessToken(account.getUserId().toString(), token);

        return response;
    }

    @Override
    public void verifyCode(String email, String inputCode) {
        String key = "email:code:" + email;
        String correctCode = redisTemplate.opsForValue().get(key);

        if (correctCode == null) {
            throw new RuntimeException("验证码已过期");
        }

        if (!correctCode.equals(inputCode)) {
            throw new RuntimeException("验证码错误");
        }

        redisTemplate.delete(key);
    }

    @Override
    @Transactional
    public void resetPassword(String email, String newPassword) {
        // 1. 通过邮箱查找Mail记录
        Mail mail = mailMapper.findByEmail(email);
        if (mail == null) {
            throw new RuntimeException("邮箱不存在");
        }

        // 2. 通过authId查找AuthAccount记录
        Account account = accountMapper.findById(mail.getUserId());
        if (account == null) {
            throw new RuntimeException("用户不存在");
        }

        // 3. 更新密码（使用BCrypt加密）
        account.setPasswordHash(passwordEncoder.encode(newPassword));
        accountMapper.updateById(account);
    }
}