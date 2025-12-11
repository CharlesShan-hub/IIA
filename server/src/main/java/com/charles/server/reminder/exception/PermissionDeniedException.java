package com.charles.server.reminder.exception;

public class PermissionDeniedException extends RuntimeException {
    public PermissionDeniedException(Long userId, Long projectId) {
        super("User " + userId + " has no permission to access project " + projectId);
    }
}