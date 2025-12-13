package com.charles.server.reminder.exception;

public class ProjectAlreadyExistException extends RuntimeException {
    public ProjectAlreadyExistException(String name) {
        super("Project with name "+ name+" already exist");
    }
}