package com.charles.server.auth.exception;

import lombok.Getter;

@Getter
public class AuthException extends RuntimeException {
    private final int code;
    
    private AuthException(int code, String message) {
        super(message);
        this.code = code;
    }
    
    public static AuthException verificationCodeInvalid() {
        return new AuthException(401, "Verification code is invalid");
    }
    
    public static AuthException verificationCodeInvalid(String message) {
        return new AuthException(401, "Verification code is invalid: " + message);
    }
    
    public static AuthException verificationCodeExpired() {
        return new AuthException(401, "Verification code has expired");
    }
    
    public static AuthException invalidCredentials() {
        return new AuthException(401, "Invalid email or password");
    }
    
    public static AuthException invalidCredentials(String message) {
        return new AuthException(401, message);
    }

    public static AuthException userNotFound(String identifier) {
        return new AuthException(404, "User not found: " + identifier);
    }
    
    public static AuthException emailAlreadyRegistered(String email) {
        return new AuthException(409, "Email already registered: " + email);
    }
}