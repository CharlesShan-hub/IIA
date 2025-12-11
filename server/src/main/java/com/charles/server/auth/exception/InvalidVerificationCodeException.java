package com.charles.server.auth.exception;

public class InvalidVerificationCodeException extends VerificationCodeException {
    public InvalidVerificationCodeException() {
        super("Invalid verification code");
    }
}