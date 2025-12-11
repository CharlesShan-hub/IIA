package com.charles.server.auth.exception;

public class ExpiredVerificationCodeException extends VerificationCodeException {
    public ExpiredVerificationCodeException() {
        super("Verification code has expired");
    }
}