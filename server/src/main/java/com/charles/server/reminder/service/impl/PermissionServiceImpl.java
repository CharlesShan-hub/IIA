package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.exception.ProjectException;
import com.charles.server.reminder.exception.TagException;
import com.charles.server.reminder.exception.TaskException;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.service.PermissionService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class PermissionServiceImpl implements PermissionService {
    
    private final ProjectMapper projectMapper;
    private final TaskMapper taskMapper;
    private final TagMapper tagMapper;
    
    @Override
    public void valid(Long userId, Long resourceId, ResourceType type) {
        get(userId, resourceId, type);
    }
    
    @Override
    @SuppressWarnings("unchecked")
    public <T> T get(Long userId, Long resourceId, ResourceType type) {
        // Find and validate the resource, then return it
        Object resource = findResource(type, resourceId);
        validateResource(userId, resourceId, resource, type);
        return (T) resource;
    }
    
    private Object findResource(ResourceType type, Long resourceId) {
        switch (type) {
            case PROJECT:
                return projectMapper.findById(resourceId);
            case TASK:
                return taskMapper.findById(resourceId);
            case TAG:
                return tagMapper.findById(resourceId);
            default:
                throw new IllegalArgumentException("Unsupported resource type: " + type);
        }
    }
    
    private void validateResource(Long userId, Long resourceId, Object resource, ResourceType type) {
        if (resource == null) {
            throw createNotFoundException(type, resourceId);
        }
        
        if (!isOwner(userId, resource, type)) {
            throw createPermissionDeniedException(type, userId, resourceId);
        }
    }
    
    private boolean isOwner(Long userId, Object resource, ResourceType type) {
        switch (type) {
            case PROJECT:
                return ((Project) resource).getUserId().equals(userId);
            case TASK:
                return ((Task) resource).getUserId().equals(userId);
            case TAG:
                return ((Tag) resource).getUserId().equals(userId);
            default:
                throw new IllegalArgumentException("Unsupported resource type: " + type);
        }
    }
    
    private RuntimeException createNotFoundException(ResourceType type, Long resourceId) {
        switch (type) {
            case PROJECT:
                return ProjectException.notFound(resourceId);
            case TASK:
                return TaskException.notFound(resourceId);
            case TAG:
                return TagException.notFound(resourceId);
            default:
                return new RuntimeException(type + " not found: " + resourceId);
        }
    }
    
    private RuntimeException createPermissionDeniedException(ResourceType type, Long userId, Long resourceId) {
        switch (type) {
            case PROJECT:
                return ProjectException.permissionDenied(userId, resourceId);
            case TASK:
                return TaskException.permissionDenied(userId, resourceId);
            case TAG:
                return TagException.permissionDenied(userId, resourceId);
            default:
                return new RuntimeException("Permission denied for " + type + ": " + resourceId);
        }
    }
}