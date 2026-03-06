package com.charles.server.reminder.exception;

public class TaskAccessException extends RuntimeException {
    private TaskAccessException(String message) {
        super(message);
    }

    public static TaskAccessException notFound(Long taskId) {
        return new TaskAccessException("Task not found with id: " + taskId);
    }

    public static TaskAccessException permissionDenied(Long userId, Long taskId) {
        return new TaskAccessException("User " + userId + " has no permission to access task " + taskId);
    }
}