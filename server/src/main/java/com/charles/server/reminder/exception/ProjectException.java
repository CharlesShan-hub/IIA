package com.charles.server.reminder.exception;

import lombok.Getter;

@Getter
public class ProjectException extends RuntimeException {
    private final int code;

    private ProjectException(int code, String message) {
        super(message);
        this.code = code;
    }

    public static ProjectException badRequest(String message) {
        return new ProjectException(400, message);
    }

    public static ProjectException permissionDenied(Long userId, Long projectId) {
        return new ProjectException(403, "User " + userId + " has no permission to access project " + projectId);
    }

    public static ProjectException notFound(Long projectId) {
        return new ProjectException(404, "Project not found with id: " + projectId);
    }

    public static ProjectException nameAlreadyExists(Long userId, String name) {
        return new ProjectException(409, "Project name already exists for user " + userId + ": " + name);
    }
}