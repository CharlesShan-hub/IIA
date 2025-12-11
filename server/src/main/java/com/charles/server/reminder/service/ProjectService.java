package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.CreateProjectRequest;
import com.charles.server.reminder.dto.UpdateProjectRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /** Create a new project 
     * @param userId the user ID
     * @param dto the project creation request
    */
    void create(Long userId, CreateProjectRequest dto);

    /** Update an existing project
     * @param userId the user ID
     * @param dto the project update request
    */
    void update(Long userId, UpdateProjectRequest dto);

    /** Update the sort order of a project
     * @param userId the user ID
     * @param projectId the project ID
     * @param sortOrder the new sort order
    */
    void updateSortOrder(Long userId, Long projectId, Integer sortOrder);
    
    /** Get all projects for a user
     * @param userId the user ID
     * @return the list of projects
    */
    List<Project> getAll(Long userId);
    
    /** Get a project by ID
     * @param userId the user ID
     * @param projectId the project ID
     * @return the project
    */
    Project getProjectById(Long userId, Long projectId);

    /** Get a project by name
     * @param userId the user ID
     * @param name the project name
     * @return the project
    */
    Project getProjectByName(Long userId, String name);

    /** Get a project by sort order
     * @param userId the user ID
     * @param sortOrder the sort order
     * @return the project
    */
    Project getProjectBySortOrder(Long userId, Integer sortOrder);

    /** Check if a project exists by name
     * @param userId the user ID
     * @param name the project name
     * @return true if exists, false otherwise
    */
    boolean existsByName(Long userId, String name);

    /** Check if a project exists by sort order
     * @param userId the user ID
     * @param sortOrder the sort order
     * @return true if exists, false otherwise
    */
    public boolean existsBySortOrder(Long userId, Integer sortOrder);

    /** Batch update the sort order of projects
     * @param userId the user ID
     * @param request the batch update position request
    */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest request);
}