package com.charles.server.auth.exception;

public class InvalidTokenException extends TokenException {
    public InvalidTokenException() {
        super("Invalid token");
    }

    public InvalidTokenException(String message) {
        super(message);
    }
}