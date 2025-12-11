package com.charles.server.auth.exception;

public class InvalidCredentialsException extends AuthenticationException {
    public InvalidCredentialsException() {
        super("Invalid email or password");
    }

    public InvalidCredentialsException(String message) {
        super(message);
    }
}
