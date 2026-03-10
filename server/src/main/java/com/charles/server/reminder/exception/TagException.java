package com.charles.server.reminder.exception;

public class TagException extends RuntimeException {
    private TagException(String message) {
        super(message);
    }

    private TagException(String message, Throwable cause) {
        super(message, cause);
    }

    public static TagException notFound(Long tagId) {
        return new TagException("Tag not found with id: " + tagId);
    }

    public static TagException permissionDenied(Long userId, Long tagId) {
        return new TagException("User " + userId + " has no permission to access tag " + tagId);
    }

    public static TagException nameAlreadyExists(Long userId, String name) {
        return new TagException("Tag name already exists for user " + userId + ": " + name);
    }

    public static TagException createFailed(Long userId, Throwable cause) {
        return new TagException("Error creating tag for user " + userId, cause);
    }

    public static TagException updateFailed(Long userId, Long tagId, Throwable cause) {
        return new TagException("Error updating tag " + tagId + " for user " + userId, cause);
    }

    public static TagException deleteFailed(Long userId, Long tagId, Throwable cause) {
        return new TagException("Error deleting tag " + tagId + " for user " + userId, cause);
    }
}