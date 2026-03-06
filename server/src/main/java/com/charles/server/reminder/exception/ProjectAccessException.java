package com.charles.server.reminder.exception;

public class ProjectAccessException extends RuntimeException {
    private ProjectAccessException(String message) {
        super(message);
    }

    public static ProjectAccessException notFound(Long projectId) {
        return new ProjectAccessException("Project not found with id: " + projectId);
    }

    public static ProjectAccessException permissionDenied(Long userId, Long projectId) {
        return new ProjectAccessException("User " + userId + " has no permission to access project " + projectId);
    }
}