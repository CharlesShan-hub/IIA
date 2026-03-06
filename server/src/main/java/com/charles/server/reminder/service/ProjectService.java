package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.CreateProjectRequest;
import com.charles.server.reminder.dto.UpdateProjectRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.DeleteProjectRequest;
import com.charles.server.reminder.dto.GetAllProjectRequest;
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

    /** Get projects by archived filter via DTO: archived or isAll
     * @param userId the user ID
     * @param dto query options
     * @return the list of projects matching the filter
     */
    List<Project> getAll(Long userId, GetAllProjectRequest dto);

    /** Delete a project
     * @param userId the user ID
     * @param dto the project deletion request
     */
    void delete(Long userId, DeleteProjectRequest dto);

    /** Batch update the sort order of projects
     * @param userId the user ID
     * @param dto the batch update position request
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest dto);
}