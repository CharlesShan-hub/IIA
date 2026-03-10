package com.charles.server.reminder.exception;

import lombok.Getter;

@Getter
public class TagException extends RuntimeException {
    private final int code;

    private TagException(int code, String message) {
        super(message);
        this.code = code;
    }

    private TagException(int code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
    }

    public static TagException badRequest(String message) {
        return new TagException(400, message);
    }

    public static TagException permissionDenied(Long userId, Long tagId) {
        return new TagException(403, "User " + userId + " has no permission to access tag " + tagId);
    }

    public static TagException notFound(Long tagId) {
        return new TagException(404, "Tag not found with id: " + tagId);
    }

    public static TagException nameAlreadyExists(Long userId, String name) {
        return new TagException(409, "Tag name already exists for user " + userId + ": " + name);
    }

    public static TagException createFailed(Long userId, Throwable cause) {
        return new TagException(500, "Error creating tag for user " + userId, cause);
    }

    public static TagException updateFailed(Long userId, Long tagId, Throwable cause) {
        return new TagException(500, "Error updating tag " + tagId + " for user " + userId, cause);
    }

    public static TagException deleteFailed(Long userId, Long tagId, Throwable cause) {
        return new TagException(500, "Error deleting tag " + tagId + " for user " + userId, cause);
    }
}