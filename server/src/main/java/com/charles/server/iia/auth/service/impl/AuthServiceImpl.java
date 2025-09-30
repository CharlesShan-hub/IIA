package com.charles.server.iia.auth.service.impl;

import com.charles.server.iia.auth.dto.LoginDTO;
import com.charles.server.iia.auth.dto.RegisterDTO;
import com.charles.server.iia.auth.entity.AuthAccount;
import com.charles.server.iia.auth.entity.Mail;
import com.charles.server.iia.auth.entity.Profile;
import com.charles.server.iia.auth.mapper.AuthAccountMapper;
import com.charles.server.iia.auth.mapper.MailMapper;
import com.charles.server.iia.auth.mapper.ProfileMapper;
import com.charles.server.iia.auth.service.AuthService;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.password.PasswordEncoder;
import java.util.Random;
import java.util.concurrent.TimeUnit;


@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final AuthAccountMapper authAccountMapper;
    private final ProfileMapper profileMapper;
    private final MailMapper mailMapper;
    private final PasswordEncoder passwordEncoder;
    private final JavaMailSender mailSender;
    private final StringRedisTemplate redisTemplate;
    
    @Value("${spring.mail.username}")
    private String fromEmail;

    @Override
    public AuthAccount login(LoginDTO dto) {
        // 1. 通过邮箱查找Mail记录
        Mail mail = mailMapper.findByEmail(dto.getEmail());
        if (mail == null) {
            throw new RuntimeException("邮箱不存在");
        }
        
        // 2. 通过authId查找AuthAccount记录
        AuthAccount account = authAccountMapper.findById(mail.getAuthId());
        if (account == null || !passwordEncoder.matches(dto.getPassword(), account.getPasswordHash())) {
            throw new RuntimeException("邮箱或密码错误");
        }
        
        return account;
    }

    @Override
    @Transactional
    public AuthAccount register(RegisterDTO dto) {
        // 1. 校验验证码
        if(!this.verifyCode(dto.getEmail(), dto.getCode())){
            throw new RuntimeException("验证码错误");
        }

        // 2. 检查邮箱是否已被注册
        if (mailMapper.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("邮箱已被注册");
        }

        // 3. 新的注册流程：先创建认证信息
        AuthAccount account = new AuthAccount();
        account.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        authAccountMapper.insert(account); // 插入后id会自动设置到account对象
        
        // 4. 创建用户基本信息，使用authAccount的id作为profile的id
        Profile profile = new Profile();
        // 优先使用前端传来的昵称，如果为空则使用邮箱前缀
        String nickname = dto.getNickname();
        if (nickname == null || nickname.trim().isEmpty()) {
            // 使用邮箱前缀作为默认昵称
            nickname = dto.getEmail().split("@")[0];
        }
        profile.setId(account.getId()); // 直接使用认证ID作为用户ID
        profile.setNickname(nickname);
        profileMapper.insert(profile);
        
        // 5. 创建邮箱信息，关联认证信息
        Mail mail = new Mail();
        mail.setEmail(dto.getEmail());
        mail.setAuthId(account.getId()); // 关联认证ID
        mail.setIsChecked(true); // 设置为已验证
        mailMapper.insert(mail);
        
        return account;
    }

    /**
     * 发送6位数字验证码（有效期5分钟）
     */
    public void sendCode(String email) {
        // 1. 生成随机6位验证码
        String code = String.format("%06d", new Random().nextInt(999999));

        // 2. 尝试存储到Redis（5分钟过期）
        redisTemplate.opsForValue().set(
                "iia:code:" + email,
                code,
                5, TimeUnit.MINUTES
        );

        // 3. 发送邮件
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(fromEmail);
        message.setTo(email);
        message.setSubject("[IIA] 您的验证码");
        message.setText("验证码：" + code + "（5分钟内有效）");
        mailSender.send(message);
    }

    /**
     * 校验验证码
     */
    @Override
    public boolean verifyCode(String email, String inputCode) {
        String key = "iia:code:" + email;
        String correctCode = redisTemplate.opsForValue().get(key);

        if (correctCode == null) {
            throw new RuntimeException("验证码已过期");
        }

        if (!correctCode.equals(inputCode)) {
            throw new RuntimeException("验证码错误");
        }

        // 验证成功后删除缓存
        redisTemplate.delete(key);
        return true;
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
        AuthAccount account = authAccountMapper.findById(mail.getAuthId());
        if (account == null) {
            throw new RuntimeException("用户不存在");
        }
        
        // 3. 更新密码（使用BCrypt加密）
        account.setPasswordHash(passwordEncoder.encode(newPassword));
        authAccountMapper.updateById(account);
    }
}