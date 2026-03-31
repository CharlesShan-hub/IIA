package com.charles.server.auth.service;

import com.charles.server.auth.dto.SendCodeVO;

public interface MailService {
    /**
     * Send verification code to email
     * @param email recipient email
     * @return the generated verification code
     */
    SendCodeVO sendVerificationCode(String email);
    
    /**
     * Verify the input code against the stored code
     * @param email recipient email
     * @param inputCode code entered by user
     * @throws RuntimeException if verification fails
     */
    void verifyCode(String email, String inputCode);
}