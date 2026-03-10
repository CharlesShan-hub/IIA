package com.charles.server.auth.exception;

import lombok.Getter;

@Getter
public class TokenException extends RuntimeException {
    private final int code;

    private TokenException(int code, String message) {
        super(message);
        this.code = code;
    }

    public static TokenException invalid() {
        return new TokenException(401, "Invalid token");
    }

    public static TokenException invalid(String message) {
        return new TokenException(401, "Invalid token: " + message);
    }

    public static TokenException expired() {
        return new TokenException(401, "Token has expired");
    }
}