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

    /** Get all active projects for a user
     * @param userId the user ID
     * @return the list of active projects
    */
    List<Project> getAllActive(Long userId);

    /** Get all archived projects for a user
     * @param userId the user ID
     * @return the list of archived projects
    */
    List<Project> getAllArchived(Long userId);

    /** Batch update the sort order of projects
     * @param userId the user ID
     * @param dto the batch update position request
    */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest dto);
}