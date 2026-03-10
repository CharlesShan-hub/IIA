package com.charles.server.auth.service.impl;

import com.charles.server.auth.exception.AuthException;
import com.charles.server.auth.service.MailService;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import java.util.Random;
import java.util.concurrent.TimeUnit;

import lombok.RequiredArgsConstructor;
import static java.util.Objects.requireNonNull;

@Slf4j
@Service
@RequiredArgsConstructor
public class MailServiceImpl implements MailService {

    private final StringRedisTemplate redisTemplate;
    private final JavaMailSender mailSender;

    @Value("${spring.mail.username}")
    private String fromEmail;

    @Value("${spring.mail.expiration}")
    private int codeExpiration;

    private String generateVerificationCode(){
        return String.format("%06d", new Random().nextInt(999999));
    }

    @Override
    public void sendVerificationCode(String email) {
        log.info("Sending verification code to: {}", email);
        
        // 1. Generate a 6-digit verification code
        String code = requireNonNull(generateVerificationCode(), "verification code must not be null");
        
        // 2. Cache the code in Redis with an n-minute expiration
        String key = "email:code:" + requireNonNull(email, "email must not be null");
        redisTemplate.opsForValue().set(key, code, codeExpiration, TimeUnit.MINUTES);
        
        // 3. Send the email with the verification code
        try {
            MimeMessage mimeMessage = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true, "UTF-8");
            helper.setFrom(requireNonNull(fromEmail, "fromEmail must not be null"));
            helper.setTo(email);
            helper.setSubject("Verification Code - Your Account");
            String htmlContent = requireNonNull(buildHtmlEmailContent(code), "htmlContent must not be null");
            helper.setText(htmlContent, true); // true indicates HTML
            mailSender.send(mimeMessage);
            log.info("Verification code sent successfully to: {}", email);
        } catch (MessagingException e) {
            log.error("Failed to send verification code to: {}, error: {}", email, e.getMessage(), e);
            throw new RuntimeException("Failed to send verification code: " + e.getMessage());
        }
        
        // 4. Log the code for debugging purposes (remove in production)
        log.info("Generated verification code for {}: {}", email, code);
    
    }
    
    @Override
    public void verifyCode(String email, String inputCode) {
        log.info("Verifying code for email: {}", email);
        
        String key = "email:code:" + email;
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
        redisTemplate.delete(key);
        log.info("Verification code validated successfully for email: {}", email);
    }

        private String buildHtmlEmailContent(String verificationCode) {
        return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Verification Code</title>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }
                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        padding: 30px;
                    }
                    .header {
                        text-align: center;
                        margin-bottom: 30px;
                    }
                    .logo {
                        font-size: 28px;
                        font-weight: bold;
                        color: #4a6cf7;
                        margin-bottom: 10px;
                    }
                    .title {
                        font-size: 24px;
                        color: #333;
                        margin-bottom: 20px;
                    }
                    .code-container {
                        background-color: #f8f9fa;
                        border: 2px dashed #4a6cf7;
                        border-radius: 8px;
                        padding: 20px;
                        text-align: center;
                        margin: 25px 0;
                    }
                    .verification-code {
                        font-size: 32px;
                        font-weight: bold;
                        letter-spacing: 5px;
                        color: #4a6cf7;
                        font-family: 'Courier New', monospace;
                    }
                    .instructions {
                        color: #666;
                        line-height: 1.6;
                        margin-bottom: 25px;
                    }
                    .footer {
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        color: #888;
                        font-size: 14px;
                    }
                    .warning {
                        color: #e74c3c;
                        font-weight: bold;
                        background-color: #ffeaea;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 15px 0;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">Intelligent Information Assistant</div>
                        <h1 class="title">Email Verification</h1>
                    </div>
                    <p class="instructions">
                        Hello,<br><br>
                        You've requested a verification code for your account.
                        Please use the code below to complete your verification process.
                    </p>
                    <div class="code-container">
                        <div class="verification-code">%s</div>
                    </div>
                    <div class="warning">
                        ⚠️ This code will expire in <strong>%s minutes</strong>.
                        Please do not share this code with anyone.
                    </div>
                    <p class="instructions">
                        If you didn't request this code, please ignore this email or contact our support team.
                    </p>
                    <div class="footer">
                        <p>© 2024 Your App Name. All rights reserved.</p>
                        <p>This is an automated message, please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """.formatted(verificationCode, codeExpiration);
    }
}