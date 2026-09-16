package com.charles.server.auth.service.impl;

import com.charles.server.auth.dto.SendCodeVO;
import com.charles.server.auth.exception.AuthException;
import com.charles.server.auth.service.MailService;
import com.charles.server.config.AppConfig;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import java.util.Random;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import lombok.RequiredArgsConstructor;
import static java.util.Objects.requireNonNull;

@Slf4j
@Service
@RequiredArgsConstructor
public class MailServiceImpl implements MailService {

    private final StringRedisTemplate redisTemplate;
    private final JavaMailSender mailSender;
    private final AppConfig appConfig;
    private final TemplateEngine templateEngine;

    @Value("${spring.mail.username}")
    private String fromEmail;

    @Value("${spring.mail.expiration}")
    private int codeExpiration;

    @Value("${spring.redis.key-prefix:iia:}")
    private String redisKeyPrefix;

    private String withPrefix(String key) {
        if (!StringUtils.hasText(redisKeyPrefix)) {
            return key;
        }
        if (redisKeyPrefix.endsWith(":")) {
            return redisKeyPrefix + key;
        }
        return redisKeyPrefix + ":" + key;
    }

    private String generateVerificationCode(){
        return String.format("%06d", new Random().nextInt(999999));
    }

    @Override
    public SendCodeVO sendVerificationCode(String email) {
        log.info("Sending verification code to: {}", email);
        
        // 1. Generate a 6-digit verification code
        String code = requireNonNull(generateVerificationCode(), "verification code must not be null");
        
        // 2. Cache the code in Redis with an n-minute expiration (同步操作，确保验证码可用)
        String key = requireNonNull(withPrefix("email:code:" + requireNonNull(email, "email must not be null")), "redis key must not be null");
        redisTemplate.opsForValue().set(key, code, codeExpiration, TimeUnit.MINUTES);
        
        // 3. Async send email verification code
        sendEmailAsync(email, code);
        
        // 4. Return the generated code
        if (appConfig.isMockEmail()) {
            log.info("Mock email mode enabled. Skipping real email sending for: {}", email);
            log.info("Mock email content: Verification code for {} is: {}", email, code);
            return new SendCodeVO(code);
        } else {
            return new SendCodeVO(null);
        }
    }
    
    @Async("mailTaskExecutor")
    public CompletableFuture<Void> sendEmailAsync(String email, String code) {
        try {
            log.info("Starting async email sending to: {}", email);
            
            MimeMessage mimeMessage = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true, "UTF-8");
            helper.setFrom(requireNonNull(fromEmail, "fromEmail must not be null"));
            helper.setTo(requireNonNull(email, "email must not be null"));
            helper.setSubject("Verification Code - Your Account");
            Context context = new Context();
            context.setVariable("code", code);
            context.setVariable("expiration", codeExpiration);
            String htmlContent = requireNonNull(
                templateEngine.process("mail/verification-code", context),
                "htmlContent must not be null");
            helper.setText(htmlContent, true); // true indicates HTML
            mailSender.send(mimeMessage);
            
            log.info("Async email sent successfully to: {}", email);
            return CompletableFuture.completedFuture(null);
        } catch (MessagingException e) {
            log.error("Failed to send async email to: {}, error: {}", email, e.getMessage(), e);
            return CompletableFuture.failedFuture(e);
        }
    }
    
    @Override
    public void verifyCode(String email, String inputCode) {
        log.info("Verifying code for email: {}", email);
        
        String key = requireNonNull(withPrefix("email:code:" + requireNonNull(email, "email must not be null")), "redis key must not be null");
        String correctCode = redisTemplate.opsForValue().get(key);
        
        if (correctCode == null) {
            log.warn("Verification code expired for email: {}", email);
            throw AuthException.verificationCodeExpired();
        }

        if (!correctCode.equals(inputCode)) {
            log.warn("Invalid verification code for email: {}", email);
            throw AuthException.verificationCodeInvalid();
        }
        
        // Delete the code from Redis after successful verification
        redisTemplate.delete(requireNonNull(key, "redis key must not be null"));
        log.info("Verification code validated successfully for email: {}", email);
    }

}