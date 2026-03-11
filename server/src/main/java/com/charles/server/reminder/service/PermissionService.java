package com.charles.server.reminder.service;

import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.Task;

public interface PermissionService {
    
    enum ResourceType {
        PROJECT,
        TASK,
        TAG
    }
    
    /**
     * Validate if user has permission to access the resource.
     * Throws appropriate exception (ProjectException/TaskException/TagException) if not.
     */
    void valid(Long userId, Long resourceId, ResourceType type);
    
    /**
     * Get resource with permission validation.
     * Uses internal mapper to find the resource.
     * 
     * @param userId user ID
     * @param resourceId resource ID
     * @param type resource type
     * @param <T> resource entity type (Project, Task, Tag, etc.)
     * @return the resource entity if found and user has permission
     * @throws RuntimeException appropriate domain exception if resource not found or permission denied
     */
    <T> T get(Long userId, Long resourceId, ResourceType type);
    
    // ========== Convenience methods ==========
    
    default void validProject(Long userId, Long projectId) {
        valid(userId, projectId, ResourceType.PROJECT);
    }
    
    default void validTask(Long userId, Long taskId) {
        valid(userId, taskId, ResourceType.TASK);
    }
    
    default void validTag(Long userId, Long tagId) {
        valid(userId, tagId, ResourceType.TAG);
    }
    
    default Project getProject(Long userId, Long projectId) {
        return get(userId, projectId, ResourceType.PROJECT);
    }
    
    default Task getTask(Long userId, Long taskId) {
        return get(userId, taskId, ResourceType.TASK);
    }
    
    default Tag getTag(Long userId, Long tagId) {
        return get(userId, tagId, ResourceType.TAG);
    }
}