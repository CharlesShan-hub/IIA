package com.charles.server.auth.exception;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String email) {
        super("User not found with email: " + email);
    }

    public UserNotFoundException(Long userId) {
        super("User not found with id: " + userId);
    }
}