package com.charles.server.auth.service.impl;

import com.charles.server.auth.service.MailService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import java.util.Random;
import java.util.concurrent.TimeUnit;
import lombok.RequiredArgsConstructor;

@Slf4j
@Service
@RequiredArgsConstructor
public class MailServiceImpl implements MailService {

    private final StringRedisTemplate redisTemplate;
    private final JavaMailSender mailSender;

    @Value("${spring.mail.username}")
    private String fromEmail;

    @Override
    public void sendVerificationCode(String email) {
        log.info("Sending verification code to: {}", email);
        
        // 1. Generate a 6-digit verification code
        String code = String.format("%06d", new Random().nextInt(999999));
        
        // 2. Cache the code in Redis with a 5-minute expiration
        String key = "email:code:" + email;
        redisTemplate.opsForValue().set(key, code, 5, TimeUnit.MINUTES);
        
        // 3. Send the email with the verification code
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(fromEmail);
        message.setTo(email);
        message.setSubject("Verification Code");
        message.setText("Your verification code is: " + code + ", valid for 5 minutes.");
        
        try {
            mailSender.send(message);
            log.info("Verification code sent successfully to: {}", email);
        } catch (Exception e) {
            log.error("Failed to send verification code to: {}, error: {}", email, e.getMessage(), e);
            throw new RuntimeException("Failed to send verification code: " + e.getMessage());
        }
    
    }
    
    @Override
    public void verifyCode(String email, String inputCode) {
        log.info("Verifying code for email: {}", email);
        
        String key = "email:code:" + email;
        String correctCode = redisTemplate.opsForValue().get(key);
        
        if (correctCode == null) {
            log.warn("Verification code expired for email: {}", email);
            throw new RuntimeException("Verification code expired");
        }
        
        if (!correctCode.equals(inputCode)) {
            log.warn("Invalid verification code for email: {}", email);
            throw new RuntimeException("Invalid verification code");
        }
        
        // Delete the code from Redis after successful verification
        redisTemplate.delete(key);
        log.info("Verification code validated successfully for email: {}", email);
        
    }
}