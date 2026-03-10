package com.charles.server.reminder.exception;

import lombok.Getter;

@Getter
public class TaskException extends RuntimeException {
    private final int code;

    private TaskException(int code, String message) {
        super(message);
        this.code = code;
    }

    private TaskException(int code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
    }

    public static TaskException badRequest(String message) {
        return new TaskException(400, message);
    }

    public static TaskException permissionDenied(Long userId, Long taskId) {
        return new TaskException(403, "User " + userId + " has no permission to access task " + taskId);
    }

    public static TaskException notFound(Long taskId) {
        return new TaskException(404, "Task not found with id: " + taskId);
    }

    public static TaskException conflict(String message) {
        return new TaskException(409, message);
    }

    public static TaskException serverError(String message, Throwable cause) {
        return new TaskException(500, message, cause);
    }
}