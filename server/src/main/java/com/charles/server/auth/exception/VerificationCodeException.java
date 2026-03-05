package com.charles.server.auth.exception;

public class VerificationCodeException extends RuntimeException {
    public VerificationCodeException(String message) {
        super(message);
    }
    
    public static VerificationCodeException expired() {
        return new VerificationCodeException("Verification code has expired");
    }
    
    public static VerificationCodeException invalid() {
        return new VerificationCodeException("Invalid verification code");
    }
}