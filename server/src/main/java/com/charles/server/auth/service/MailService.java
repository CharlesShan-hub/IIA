package com.charles.server.auth.service;

public interface MailService {
    /**
     * Send verification code to email
     * @param email recipient email
     */
    void sendVerificationCode(String email);
    
    /**
     * Verify the input code against the stored code
     * @param email recipient email
     * @param inputCode code entered by user
     * @throws RuntimeException if verification fails
     */
    void verifyCode(String email, String inputCode);
}