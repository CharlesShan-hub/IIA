package com.charles.server.auth.exception;

public class VerificationCodeException extends RuntimeException {
    public VerificationCodeException(String message) {
        super(message);
    }
}