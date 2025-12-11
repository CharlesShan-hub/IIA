package com.charles.server.auth.exception;

public class EmailAlreadyRegisteredException extends RegistrationException {
    public EmailAlreadyRegisteredException(String email) {
        super("Email already registered: " + email);
    }
}