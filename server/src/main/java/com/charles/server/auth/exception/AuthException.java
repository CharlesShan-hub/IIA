package com.charles.server.auth.exception;

public class AuthException extends RuntimeException {
    private final ErrorType errorType;
    
    public enum ErrorType {
        INVALID_CREDENTIALS,
        EMAIL_ALREADY_REGISTERED,
        USER_NOT_FOUND,
        VERIFICATION_CODE_INVALID
    }
    
    private AuthException(String message, ErrorType errorType) {
        super(message);
        this.errorType = errorType;
    }
    
    public ErrorType getErrorType() {
        return errorType;
    }
    
    // Static factory methods for different error types
    
    public static AuthException invalidCredentials() {
        return new AuthException("Invalid email or password", ErrorType.INVALID_CREDENTIALS);
    }
    
    public static AuthException invalidCredentials(String message) {
        return new AuthException(message, ErrorType.INVALID_CREDENTIALS);
    }
    
    public static AuthException emailAlreadyRegistered(String email) {
        return new AuthException("Email already registered: " + email, ErrorType.EMAIL_ALREADY_REGISTERED);
    }
    
    public static AuthException userNotFound(String identifier) {
        return new AuthException("User not found: " + identifier, ErrorType.USER_NOT_FOUND);
    }
    
    public static AuthException verificationCodeInvalid() {
        return new AuthException("Verification code is invalid", ErrorType.VERIFICATION_CODE_INVALID);
    }
    
    public static AuthException verificationCodeInvalid(String message) {
        return new AuthException("Verification code is invalid: " + message, ErrorType.VERIFICATION_CODE_INVALID);
    }
    
    public static AuthException verificationCodeExpired() {
        return new AuthException("Verification code has expired", ErrorType.VERIFICATION_CODE_INVALID);
    }
}