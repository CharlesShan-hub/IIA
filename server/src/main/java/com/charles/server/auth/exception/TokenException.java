package com.charles.server.auth.exception;

public class TokenException extends RuntimeException {
    public TokenException(String message) {
        super(message);
    }
    
    public static TokenException invalid() {
        return new TokenException("Invalid token");
    }
    
    public static TokenException invalid(String message) {
        return new TokenException("Invalid token: " + message);
    }
    
    public static TokenException expired() {
        return new TokenException("Token has expired");
    }
}